from enum import Enum


class TimeConstants:
    """
    Константы времени.
    """

    # Таймзона по умолчанию
    DEFAULT_TIMEZONE: str = "Asia/Yekaterinburg"


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


# Макс. кол-во строк загружаемых отзывов
#   для не-премиум пользователей
ALLOWED_NUM_ROWS: int = 500

# Если нет определенных данных в анализе
NOT_EXCEL_DATA: str = "Нет данных"
