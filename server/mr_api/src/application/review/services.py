import logging
from dataclasses import asdict, dataclass

from fastapi import UploadFile

from src.adapters.api.analyze import schemas
from src.adapters.database.settings import settings as db_settings
from src.adapters.rpc.settings import settings as io_settings
from src.application import exceptions
from src.application.constants import SourceType, Status, TimeConstants
from src.application.review import entities, interfaces
from src.application.utils import (
    datetime_to_json,
    get_current_dt,
    is_file_empty,
    is_not_valid_file_format,
    save_file,
    validate_non_empty_fields,
)

logging.config.dictConfig(db_settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@dataclass
class ReviewProcessingService:
    """
    Сервис подготовки отзывов для анализа.

    Этот сервис предоставляет функциональность
    для подготовки отзывов к анализу.
    """

    analyze_repo: interfaces.IAnalyzeRepository
    review_producer: interfaces.IReviewProducer
    analyze_consumer: interfaces.IAnalyzeConsumer
    websocket_manager: interfaces.IWebSocketManager
    excel_manager: interfaces.ExcelManager

    async def process_test_reviews(
        self,
        test: schemas.TestReviews,
    ) -> schemas.AnalyzeResponse:
        """
        Подготавливает тестовые отзывы для дальнейшего анализа.

        :param test: Объект, содержащий список тестовых отзывов для анализа.

        :return: Результаты анализа тестовых отзывов.

        :raises EmptyFieldException: Если хотя бы одно поле
        тестовых отзывов пустое.
        :raises TooManyTestReviewsException: Если количество тестовых
        отзывов превышает 10 штук.
        :raises ReviewsProcessingException: Если произошла ошибка
        при обработке тестовых отзывов.
        :raises AnalyzeServiceException: Если в сервисе анализа случилась
        ошибка.
        """

        # Валидация непустых полей в тесте
        empty_field = validate_non_empty_fields(test.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        # Проверка на количество тестовых отзывов
        if len(test.reviews) > 10:
            raise exceptions.TooManyTestReviewsException

        try:
            # Подготовка тестовых отзывов для отправки
            prepared_reviews = [
                asdict(
                    entities.ReviewTemplate(
                        number=index,
                        message=review.strip(),
                        author="You"
                    )
                )
                for index, review in enumerate(test.reviews, start=1)
            ]

            # Отправка тестовых отзывов в очередь для анализа
            await self.review_producer.send_reviews(
                prepared_reviews, io_settings.REVIEW_QUEUE_NAME
            )
            logger.info("Тестовые отзывы отправлены в сервис анализа отзывов")

            # Ожидание и получение результатов анализа из очереди
            async with self.analyze_consumer as consumer:
                async for analyze_results in consumer.receive_analyze_results(
                    io_settings.ANALYZE_QUEUE_NAME
                ):
                    logger.info("Получен результат анализа тестовых отзывов")

                    # Если в сервисе анализов произошла ошибка,
                    #   то вернет нам статус с ошибкой
                    if analyze_results["status"] == Status.ERROR.value:
                        raise exceptions.AnalyzeServiceException

                    # Формирование и возврат ответа с результатами анализа
                    return schemas.AnalyzeResponse(
                        dt=datetime_to_json(
                            get_current_dt(TimeConstants.DEFAULT_TIMEZONE)
                        ),
                        source_type=SourceType.TEST.value,
                        entries_analyze=analyze_results["entries_analyze"],
                        full_analyze=analyze_results["full_analyze"],
                        status=Status.COMPLETE.value
                    )
        except Exception as e:
            logger.exception(
                "Произошла ошибка при обработке тестовых отзывов: %s", str(e)
            )
            raise exceptions.ReviewsProcessingException

    async def process_reviews_from_file_middleware(
        self,
        file: UploadFile
    ) -> None:

        # Проверка формата загруженного файла
        if is_not_valid_file_format(file.filename):
            raise exceptions.InvalidFileFormatException

        ws = self.excel_manager.load_data(file.file)

        # Проверка на пустоту файла
        if is_file_empty(ws):
            raise exceptions.FileEmptyException

        return None

    async def process_reviews_from_file(
        self,
        file: UploadFile,
        user_id: int
    ) -> schemas.AnalyzeResponse | None:
        """
        Обрабатывает отзывы из загруженного файла.

        :param file: Загруженный файл с отзывами.
        :param user_id: Идентификатор пользователя, загрузившего файл.

        :return: Результат анализа отзывов из файла или None,
        если не удалось провести анализ.

        :raises InvalidFileFormatException: Если формат файла недопустим.
        :raises FileEmptyException: Если файл пуст.
        :raises ReviewsProcessingException: Если произошла ошибка
        при обработке отзывов.
        :raises AnalyzeServiceException: Если в сервисе анализа случилась
        ошибка.
        """

        # Загрузка и чтение данных из Excel файла
        ws = self.excel_manager.load_data(file.file)

        prepared_reviews = []

        # Обработка отзывов из файла
        #   Предполагается, что отзывы находятся в первом столбце Excel файла
        for index, row in enumerate(ws.iter_rows(values_only=True), start=1):
            prepared_reviews.append(
                asdict(
                    entities.ReviewTemplate(
                        number=index,
                        message=str(row[0]).strip()
                    )
                )
            )

        # Сохранение пути к файлу на сервере
        file_path = save_file(file, user_id)

        try:
            # Отправка отзывов в очередь для анализа
            await self.review_producer.send_reviews(
                prepared_reviews, io_settings.REVIEW_QUEUE_NAME
            )
            logger.info("Отзывы из файла отправлены в сервис анализа отзывов")

            # Ожидание и получение результатов анализа из очереди
            async with self.analyze_consumer as consumer:
                async for analyze_results in consumer.receive_analyze_results(
                    io_settings.ANALYZE_QUEUE_NAME
                ):
                    logger.info("Получен результат анализа отзывов из файла")

                    # Проверка статуса результата анализа
                    if analyze_results["status"] == Status.ERROR.value:
                        raise Exception

                    # Сохранение результатов анализа в базе данных
                    analyze_result = entities.AnalyzeInput(
                        user_id=user_id,
                        dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
                        source_type=SourceType.FILE.value,
                        source_url=file_path,
                        entries_analyze=analyze_results["entries_analyze"],
                        full_analyze=analyze_results["full_analyze"],
                        status=analyze_results["status"]
                    )

                    await self.analyze_repo.save_analyze(analyze_result)

                    logger.info("Результат анализа сохранён в БД")

                    await self.websocket_manager.send_message(
                        user_id,
                        "Анализ отзывов из файла завершён."
                    )

                    return None
                    # Конвертация даты анализа в строковый формат
                    # analyze.dt = datetime_to_json(analyze.dt)
                    # return schemas.AnalyzeResponse(
                    #     **asdict(analyze)
                    # )
        except Exception as e:
            logger.exception(
                "Произошла ошибка при обработке отзывов из файла: %s", str(e)
            )

            # Сохранение ошибочного результата анализа в базе данных
            analyze_error = entities.AnalyzeInput(
                user_id=user_id,
                dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
                source_type=SourceType.FILE.value,
                source_url=file_path,
                entries_analyze=None,
                full_analyze=None,
                status=analyze_results["status"]
            )

            await self.analyze_repo.save_analyze(analyze_error)

            await self.websocket_manager.send_message(
                user_id,
                "Произошла ошибка при обработке отзывов из файла."
            )

            return None
