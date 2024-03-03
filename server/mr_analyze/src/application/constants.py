from enum import Enum


class TimeConstants:
    """
    Константы времени.
    """

    # Таймзона по умолчанию
    DEFAULT_TIMEZONE: str = "Asia/Yekaterinburg"


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


# Словарь для определения пола по тегам морфологического анализатора
GENDERS: dict = {
    "masc": "Мужчина",
    "femn": "Девушка"
}


class SentimentCategory(Enum):
    """
    Перечисление для категорий настроения.
    """
    POSITIVE: str = "Позитивный"
    NEGATIVE: str = "Негативный"
    NEUTRAL: str = "Нейтральный"


class PartOfSpeech(Enum):
    """
    Перечисление для частей речи слова.
    """
    NOUN: str = "NOUN"            #: Существительное
    VERB: str = "VERB"            #: Глагол
    ADJECTIVE: str = "ADJECTIVE"  #: Прилагательное
    ADVERB: str = "ADVERB"        #: Наречие
    OTHER: str = "OTHER"          #: Другие части речи
    UNKNOWN: str = "UNKN"         #: Неизвестно
