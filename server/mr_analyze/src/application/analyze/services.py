import logging
from dataclasses import asdict, dataclass

from src.adapters.rpc.settings import settings
from src.application.analyze import entities, interfaces
from src.application.constants import Status


@dataclass
class AnalyzeService:
    """
    Сервис для анализа отзывов.
    """

    analyze_repo: interfaces.IAnalyzeRepository
    review_consumer: interfaces.IReviewСonsumer
    analyze_producer: interfaces.IAnalyzeProducer
    nlp_service: interfaces.INLPService

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

            # Выполнение анализа сентимента,
            #   ключевых слов,
            #   пола
            #   и возраста авторов отзывов
            sentiments = self.nlp_service.analyze_sentiment(reviews)
            keywords = self.nlp_service.extract_keywords(reviews)
            authors_gender = self.nlp_service.extract_gender_author(reviews)
            authors_age = self.nlp_service.extract_age_author(reviews)

            # Подготовка результатов анализа для отправки
            entries_analyze = []
            for review in reviews:
                review_number = review.get("number")
                sentiment = sentiments.get(review_number)
                keywords_list = keywords.get(review_number)
                author_gender = authors_gender.get(review_number)
                author_age = authors_age.get(review_number)

                entry_analyze = asdict(
                    entities.EntryAnalyze(
                        number=review_number,
                        message=review.get("message"),
                        sentiment=sentiment,
                        keywords=keywords_list,
                        author_gender=author_gender,
                        author_age=author_age
                    )
                )
                entries_analyze.append(entry_analyze)

            # Формирование общих результатов анализа
            analyze_results = asdict(
                entities.AnalyzeResults(
                    entries_analyze=entries_analyze,
                    full_analyze={1: 1},
                    status=Status.COMPLETE.value
                )
            )

            logging.info("Анализ завершён")

            # Отправка результатов анализа в очередь
            await self.analyze_producer.send_analyze_results(
                analyze_results, settings.ANALYZE_QUEUE_NAME
            )
            logging.info("Результат анализа отправлен в очередь")

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
