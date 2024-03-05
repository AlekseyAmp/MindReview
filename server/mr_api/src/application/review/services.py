import logging
from dataclasses import asdict, dataclass

from fastapi import UploadFile

from src.adapters.api.analyze import schemas
from src.adapters.database.settings import settings as db_settings
from src.adapters.rpc.settings import settings as io_settings
from src.application import exceptions
from src.application.constants import (
    ALLOWED_NUM_ROWS,
    NOT_EXCEL_DATA,
    SourceType,
    Status,
    TimeConstants,
)
from src.application.review import entities
from src.application.review import interfaces as review_interfaces
from src.application.user import interfaces as user_interfaces
from src.application.utils import (
    datetime_to_json,
    get_current_dt,
    get_file_num_rows,
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

    analyze_repo: review_interfaces.IAnalyzeRepository
    user_repo: user_interfaces.IUserRepository
    review_producer: review_interfaces.IReviewProducer
    analyze_consumer: review_interfaces.IAnalyzeConsumer
    websocket_manager: review_interfaces.IWebSocketManager
    excel_manager: review_interfaces.ExcelManager

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

        return: schemas.AnalyzeResponse
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
        file: UploadFile,
        user_id: int
    ) -> None:
        """
        Подготавливает тестовые отзывы для дальнейшего анализа.

        :param file: Загруженный файл с обзорами.

        :param user_id: Идентификатор пользователя.

        :raises InvalidFileFormatException: Если формат загруженного
        файла недопустим.
        :raises FileEmptyException: Если загруженный файл пуст.
        :raises PremiumSubscriptionRequiredException: Если у пользователя
        нет премиум-подпискии количество строк в файле превышает
        ALLOWED_NUM_ROWS.

        :return: None.
        """

        # Проверка формата загруженного файла
        if is_not_valid_file_format(file.filename):
            raise exceptions.InvalidFileFormatException

        ws = self.excel_manager.load_data(file.file)

        # Проверка на пустоту файла
        if is_file_empty(ws):
            raise exceptions.FileEmptyException

        # Проверка на кол-во строк
        user = await self.user_repo.get_user_premium_by_id(user_id)
        if (
            not user.is_premium
            and get_file_num_rows(ws) > ALLOWED_NUM_ROWS
        ):
            raise exceptions.PremiumSubscriptionRequiredException(
                ALLOWED_NUM_ROWS
            )

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

        return: schemas.AnalyzeResponse | None
        """

        # Загрузка и чтение данных из Excel файла
        ws = self.excel_manager.load_data(file.file)

        prepared_reviews = list()
        unique_reviews = set()
        # Обработка отзывов из файла
        #   Предполагается, что отзывы находятся в первом столбце Excel файла
        for index, row in enumerate(ws.iter_rows(values_only=True), start=1):
            message = str(row[0]).strip()
            # Проверка на наличие дубликатов перед добавлением в множество
            if message not in unique_reviews:
                unique_reviews.add(message)
                prepared_reviews.append(
                    asdict(
                        entities.ReviewTemplate(
                            number=index,
                            message=message
                        )
                    )
                )

        # Сохранение пути к файлу на сервере
        file_path = save_file(file, user_id)

        try:
            # Отправка отзывов в очередь для анализа
            await self.review_producer.send_reviews(
                list(prepared_reviews), io_settings.REVIEW_QUEUE_NAME
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

                    analyze = await self.analyze_repo.save_analyze(
                        analyze_result
                    )

                    logger.info(
                        "Результат анализа сохранён в БД, (id - %s)",
                        str(analyze.id)
                    )

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

    async def download_analyze(
        self,
        analyze_id: int,
        user_id: int
    ) -> dict[str, str]:
        """
        Скачивает результат анализа в формате Excel.

        :param analyze_id: Идентификатор анализа.
        :param user_id: Идентификатор пользователя.

        :return: Словарь с информацией о скачанном файле.

        :raises AnalyzeNotFoundException: Если анализ с
        указанным идентификатором не найден.
        """

        analyze = await self.analyze_repo.get_analyze_by_id(
            analyze_id,
            user_id
        )

        if analyze is None:
            raise exceptions.AnalyzeNotFoundException

        logger.info("Формируем результат анализа в Excel файл.")

        analyze_dict = asdict(analyze)
        full_analyze = await self._process_full_analyze_report_data(
            analyze_dict
        )
        shot_analyze = await self._process_short_analyze_report_data(
            analyze_dict
        )

        logger.info("Excel файл с реузльтатом анализа сформирован.")

        temp_file_path = self.excel_manager.create_analyze_report(
            shot_analyze,
            full_analyze
        )

        return {
            "file_path": temp_file_path,
            "file_name": (
                "Результат анализа за "
                f"{datetime_to_json(analyze.dt)}.xlsx"
            )
        }

    async def _process_short_analyze_report_data(self, analyze: dict) -> list:
        """
        Обрабатывает данные для короткого анализа.

        :param analyze: Словарь с данными анализа.

        :return: Результат короткого анализа.
        """

        short_analyze = []

        if analyze["full_analyze"]:
            # Популярный сентимент
            sentiments_data = analyze.get(
                "full_analyze", {}
            ).get("sentiments_data", {})
            sentiments = sentiments_data.get("sentiments")
            max_sentiment_key = max(
                sentiments,
                key=lambda x: sentiments[x].get("count")
            )
            max_sentiment = sentiments[max_sentiment_key]
            sentiment_name = max_sentiment_key
            percentage = max_sentiment.get("percentage")
            most_popular_sentiment = f"{sentiment_name} ({percentage}%)"

            # Топ 5 ключевых слов
            keywords_cloud = analyze.get(
                "full_analyze", {}
            ).get("keywords_cloud", {})

            if keywords_cloud:
                top_keywords = sorted(
                    keywords_cloud.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                top_keywords_string = ", ".join(
                    [
                        f"{keyword} ({mentions})"
                        for keyword, mentions in top_keywords
                    ]
                )
            else:
                top_keywords_string = NOT_EXCEL_DATA

            # Топ 5 городов
            geographical_map = analyze.get(
                "full_analyze", {}
            ).get("geographical_map", {})

            if geographical_map:
                top_cities = sorted(
                    geographical_map.items(),
                    key=lambda x: x[1], reverse=True
                )[:5]
                top_cities_string = ", ".join(
                    [
                        f"{city} ({mentions})"
                        for city, mentions in top_cities
                    ]
                )
            else:
                top_cities_string = NOT_EXCEL_DATA

            short_analyze.append([
                datetime_to_json(analyze.get("dt", NOT_EXCEL_DATA)),
                analyze.get("source_type", NOT_EXCEL_DATA),
                analyze.get("source_url", NOT_EXCEL_DATA),
                len(analyze.get("entries_analyze", NOT_EXCEL_DATA)),
                most_popular_sentiment,
                top_keywords_string,
                top_cities_string
            ])
        else:
            short_analyze.append([NOT_EXCEL_DATA for _ in range(7)])

        return short_analyze

    async def _process_full_analyze_report_data(self, analyze: dict) -> list:
        """
        Обрабатывает данные для полного анализа.

        :param analyze: Словарь с данными анализа.

        :return: Результат полного анализа.
        """

        full_analyze = []

        if analyze["entries_analyze"]:
            for entry in analyze["entries_analyze"]:
                other_info = entry.get("other_info", {})
                cities = other_info.get("cities", {})
                years = other_info.get("years", {})
                cities_string = ", ".join(cities) if cities else NOT_EXCEL_DATA
                years_string = ", ".join(years) if years else NOT_EXCEL_DATA

                full_analyze.append([
                    entry.get("number", NOT_EXCEL_DATA),
                    entry.get("message", NOT_EXCEL_DATA),
                    ", ".join(entry.get("sentiment", NOT_EXCEL_DATA)),
                    ", ".join(entry.get("keywords", NOT_EXCEL_DATA)),
                    cities_string,
                    years_string
                ])
        else:
            full_analyze.append([NOT_EXCEL_DATA for _ in range(6)])

        return full_analyze
