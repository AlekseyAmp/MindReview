from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table

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
        'name',
        String,
        nullable=False,
        comment='Название города',
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
    comment='Таблица стоп-слов для фильтрации текстов'
)
