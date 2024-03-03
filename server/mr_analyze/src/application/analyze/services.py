import logging
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

        logging.info("Сервис анализа запущен")
        async with self.review_consumer as consumer:
            # TODO: доделать
            # reviews = await self.review_consumer.check_queue_empty(
            #     settings.REVIEW_QUEUE_NAME
            # )
            # if reviews:
            #     await self.analyze_reviews(reviews)

            # Ожидание и получение результатов анализа из очереди
            async for reviews in consumer.receive_reviews(
                settings.REVIEW_QUEUE_NAME
            ):
                logging.info("Получены новые отзывы для анализа")
                await self.analyze_reviews(reviews)

    async def analyze_reviews(self, reviews: list[dict]) -> None:
        """
        Анализирует отзывы.

        :param reviews: Список отзывов для анализа.
        """
        try:
            logging.info("Начало анализа отзывов")
            
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

            logging.info("Анализ завершён")

            # Подготавливаем результат анализа по каждому отзыву
            entries_analyze = self._prepare_entries_analyze(
                reviews,
                nlp_result
            )

            # Формирование результатов анализа
            analyze_results = asdict(
                entities.AnalyzeResults(
                    entries_analyze=entries_analyze,
                    full_analyze={1: 1},
                    status=Status.COMPLETE.value
                )
            )

            # Отправка результатов анализа в очередь
            await self.analyze_producer.send_analyze_results(
                analyze_results, settings.ANALYZE_QUEUE_NAME
            )
            logging.info("Результат анализа отправлен в очередь")

            return None
        except Exception as e:
            logging.exception(
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
                asdict(
                    entities.EntryAnalyze(
                        number=review_number,
                        raiting=review.get("raiting"),
                        message=review.get("message"),
                        sentiment=sentiment,
                        keywords=keywords_list,
                        other_info=entities.OtherInfo(
                            cities,
                            years
                        )
                    )
                )
            )

        return entries_analyze

    def _prepare_full_analyze(
        self,
        entries_analyze: list[entities.EntryAnalyze],
    ):
        pass
