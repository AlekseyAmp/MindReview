from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text

from src.adapters.database.settings import settings

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
        String,
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
