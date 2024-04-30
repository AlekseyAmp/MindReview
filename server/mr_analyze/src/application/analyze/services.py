from dataclasses import asdict, dataclass

from src.adapters.rpc.settings import settings
from src.application.analyze import entities, interfaces
from src.application.collection import interfaces as collection_interfaces
from src.application.constants import Status


@dataclass
class AnalyzeService:
    """
    Сервис для анализа отзывов.
    """

    analyze_repo: interfaces.IAnalyzeRepository
    data_repo: collection_interfaces.IDataRepository
    review_consumer: interfaces.IReviewСonsumer
    analyze_producer: interfaces.IAnalyzeProducer
    nlp_service: interfaces.INLPService
    keywords_stopwords: set[str]

    async def start_review_processing(self) -> None:
        """
        Начинает обработку отзывов из очереди.
        """

        print("Сервис анализа запущен")

        async with self.review_consumer as consumer:
            # Ожидание и получение результатов анализа из очереди
            async for reviews in consumer.receive_reviews(
                settings.REVIEW_QUEUE_NAME
            ):
                print("Получены новые отзывы для анализа")
                await self.analyze_reviews(reviews)

    async def analyze_reviews(self, reviews: list[dict]) -> None:
        """
        Анализирует отзывы.

        :param reviews: Список отзывов для анализа.
        """
        try:
            print("Начало анализа отзывов")

            # Получаем список все городов
            all_cities = self.data_repo.get_all_cities()
            self.keywords_stopwords.update(
                city.raw_name
                for city in all_cities
            )

            # Проводим анализ
            sentiments = self.nlp_service.analyze_sentiment(reviews)
            keywords = self.nlp_service.extract_keywords(
                reviews,
                self.keywords_stopwords
            )

            # Составляем стоп-ворды для городов на основе ключевых слов
            stopwords_cities = set()
            for city_keywords in keywords.values():
                stopwords_cities.update(filter(None, city_keywords))

            cities = self.nlp_service.extract_cities(
                reviews,
                all_cities,
                stopwords_cities
            )
            years = self.nlp_service.extract_years(reviews)

            nlp_result = entities.NLPResult(
                sentiments=sentiments,
                keywords=keywords,
                cities=cities,
                years=years
            )

            print("Анализ завершён")

            # Подготавливаем результат анализа по каждому отзыву
            entries_analyze = (self._prepare_entries_analyze(
                reviews,
                nlp_result
            ))
            entries_analyze_dicts = [
                asdict(entry)
                for entry in entries_analyze
            ]

            full_analyze = self._prepare_full_analyze(
                entries_analyze
            )

            # Формирование результатов анализа
            analyze_results = asdict(
                entities.AnalyzeResults(
                    entries_analyze=entries_analyze_dicts,
                    full_analyze=asdict(full_analyze),
                    status=Status.COMPLETE.value
                )
            )

            # Отправка результатов анализа в очередь
            await self.analyze_producer.send_analyze_results(
                analyze_results, settings.ANALYZE_QUEUE_NAME
            )
            print("Результат анализа отправлен в очередь")

            return None
        except Exception as e:
            print(
                "Произошла ошибка при анализе отзывов: %s", str(e)
            )

            # Подготовка сообщения об ошибке для отправки
            analyze_error = asdict(
                entities.AnalyzeResults(
                    entries_analyze=None,
                    full_analyze=None,
                    status=Status.ERROR.value
                )
            )

            # Отправка сообщения об ошибке в очередь
            await self.analyze_producer.send_analyze_results(
                analyze_error, settings.ANALYZE_QUEUE_NAME
            )

            return None

    def _prepare_entries_analyze(
        self,
        reviews: list[dict],
        nlp_result: entities.NLPResult
    ) -> list:
        entries_analyze = []
        for review in reviews:
            review_number = review.get("number")
            sentiment = nlp_result.sentiments.get(review_number)
            keywords_list = nlp_result.keywords.get(review_number)
            cities = nlp_result.cities.get(review_number)
            years = nlp_result.years.get(review_number)

            entries_analyze.append(
                entities.EntryAnalyze(
                    number=review_number,
                    raiting=review.get("raiting"),
                    message=review.get("message"),
                    sentiment=sentiment,
                    keywords=keywords_list,
                    other_info=entities.OtherInfo(
                        cities if cities else [],
                        years if years else []
                    )
                )
            )

        return entries_analyze

    def _prepare_full_analyze(
        self,
        entries_analyze: list[entities.EntryAnalyze],
    ) -> entities.FullAnalyze:

        # Собираем облако ключевых слов
        keywords_cloud = {}
        for entry in entries_analyze:
            for keyword in entry.keywords:
                if keyword in keywords_cloud:
                    keywords_cloud[keyword] += 1
                else:
                    keywords_cloud[keyword] = 1

        # Собираем данные о сентименте
        sentiments_data = {
            'total': 0,
            'sentiments': {}
        }
        for entry in entries_analyze:
            if entry.sentiment:
                sentiment = entry.sentiment[0]
                sentiment_key = sentiment

                if sentiment_key not in sentiments_data['sentiments']:
                    sentiments_data['sentiments'][sentiment_key] = {'count': 0}

                sentiments_data['sentiments'][sentiment_key]['count'] += 1

                # Увеличиваем total_sentiments
                sentiments_data['total'] += 1

        # Рассчитываем процент сентиментов
        total_sentiments = sentiments_data['total']
        for sentiment_data in sentiments_data['sentiments'].values():
            percentage = (sentiment_data['count'] / total_sentiments) * 100
            sentiment_data['percentage'] = round(percentage, 2)

        # Собираем информацию о количестве упоминаний
        #   ключевых слов для каждого сентимента
        keyword_sentiment_counts = {}
        for entry in entries_analyze:
            sentiment = entry.sentiment[0]
            keywords = entry.keywords
            if sentiment not in keyword_sentiment_counts:
                keyword_sentiment_counts[sentiment] = {}
            for keyword in keywords:
                if keyword:
                    if keyword not in keyword_sentiment_counts[sentiment]:
                        keyword_sentiment_counts[sentiment][keyword] = 0
                    keyword_sentiment_counts[sentiment][keyword] += 1

        # Собираем информацию о количестве упоминаний городов
        #   (географическая карта)
        geographical_map = {}
        for entry in entries_analyze:
            if entry.other_info.cities:
                for city in entry.other_info.cities:
                    geographical_map[city] = geographical_map.get(city, 0) + 1

        return entities.FullAnalyze(
            keywords_cloud=keywords_cloud,
            sentiments_data=sentiments_data,
            keyword_sentiment_counts=keyword_sentiment_counts,
            geographical_map=geographical_map
        )
