from sqlalchemy import Column, DateTime, Integer, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import ENUM

from src.adapters.database.settings import settings
from src.application.constants import LogLevel

metadata = MetaData(schema=settings.SCHEMAS["logs"])

logs = Table(
    'logs',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор лога',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        comment='Метка времени лога',
    ),
    Column(
        'level',
        ENUM(
            *[log_level.value for log_level in LogLevel],
            name='log_level_enum',
        ),
        nullable=False,
        comment='Уровень важности лога',
    ),
    Column(
        'message',
        Text,
        nullable=False,
        comment='Сообщение лога',
    ),
    comment='Таблица, содержащая логи приложения.',
)
