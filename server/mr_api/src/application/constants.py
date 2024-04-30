from enum import Enum


class TimeConstants:
    """
    Константы времени.
    """

    # Таймзона по умолчанию
    DEFAULT_TIMEZONE: str = "Asia/Yekaterinburg"


class ReviewsURLConstants:
    """
    Константы URL сайтов с отзывами.
    """

    # URL для отзывов Wildberries
    WB_FEEDBACK_URL: str = "https://feedbacks1.wb.ru/feedbacks/v1/"


class ReviewWebsite(Enum):
    """
    Перечисление для сайтов с отзывовами.
    """

    WILDBERRIES: str = "Wildberries"


class FileConstants:
    """
    Константы для обработки файлов.
    """

    # Путь к директории для загрузки файлов
    UPLOAD_DIR: str = "./USER_FILES"

    # Разрешенные форматы файл
    ALLOWED_FORMATS: list[str] = ['.xlsx']


class UserRole(Enum):
    """
    Перечисление для ролей пользователей.
    """
    USER: str = "user"
    ADMIN: str = "admin"


class SourceType(Enum):
    """
    Перечисление для типов источников загрузки отзывов.
    """
    TEST: str = "test"
    FILE: str = "file"
    WEBSITE: str = "website"


class Status(Enum):
    """
    Перечисление для статусов формирования анализа.
    """
    COMPLETE: str = "complete"
    ERROR: str = "error"


class LogLevel(Enum):
    """
    Уровни важности лога
    """
    DEBUG: str = "debug"
    INFO: str = "info"
    WARNING: str = "warning"
    ERROR: str = "error"
    CRITICAL: str = "critical"


# Если нет определенных данных в анализе
NOT_EXCEL_DATA: str = "Нет данных"

# Макс. кол-во строк загружаемых отзывов
ALLOWED_NUM_ROWS: int = 500


class PremiumSubscriptionRequiredTypes(Enum):
    """
    Перечисление того, чего нельзя делать
    не-премиум пользователям.
    """

    # Тип: Скачивать отчёт
    DOWNLOAD: str = "download"

    # Тип: Максимальное кол-во строк отзывов,
    #   которые можно анализировать
    MAX_ROWS: str = "max_rows"


class SystemConstants:
    """
    Константы для информации о системе.
    """

    # Общее
    SYSTEM_VERSION: str = "0.1"

    # Клиент
    CLIENT_HOST: str = "http://localhost:3000"

    # Сервер
    API_HOST: str = "http://localhost:8000"
    API_DOCS: str = "http://localhost:8000/docs"
    WS_HOST: str = "ws://localhost:8000/api"
    RABBITMQ_HOST: str = "http://localhost:15672"
