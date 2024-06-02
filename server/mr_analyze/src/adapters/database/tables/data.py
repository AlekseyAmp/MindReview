from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
)

from src.adapters.database.settings import settings
from src.application.constants import TimeConstants
from src.application.utils import get_current_dt

metadata = MetaData(schema=settings.SCHEMAS["data"])

cities = Table(
    'cities',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор города',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        default=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
        comment='Дата добавления города',
    ),
    Column(
        'raw_name',
        String,
        nullable=False,
        unique=True,
        comment='Сырое имя города',
    ),
    Column(
        'original_name',
        String,
        nullable=True,
        comment='Оригинальное название города',
    ),
    comment='Список городов для распознавания города в отзыве'
)

stopwords = Table(
    'stopwords',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор стоп-слова',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        default=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
        comment='Дата добавления стоп-слова',
    ),
    Column(
        'word',
        String,
        nullable=False,
        unique=True,
        comment='Стоп-слово',
    ),
    Column(
        'use',
        Boolean,
        nullable=False,
        default=False,
        comment='Использовать стоп-слово или нет',
    ),
    comment='Таблица стоп-слов для фильтрации текстов'
)
