from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from src.application.constants import TimeConstants
from src.application.utils import get_current_dt

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор пользователя',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        default=get_current_dt(TimeConstants.TIMEZONE),
        comment='Дата регистрации пользователя',
    ),
    Column(
        'first_name',
        String,
        nullable=False,
        comment='Имя пользователя',
    ),
    Column(
        'last_name',
        String,
        nullable=False,
        comment='Фамилия пользователя',
    ),
    Column(
        'email',
        String,
        unique=True,
        nullable=False,
        comment='Адрес электронной почты пользователя',
    ),
    Column(
        'password',
        String,
        nullable=False,
        comment='Пароль пользователя',
    ),
    Column(
        'role',
        String,
        nullable=False,
        default='user',
        comment='Роль пользователя',
    ),
    comment='Таблица, содержащая информацию о пользователях',
)

analysis = Table(
    'analysis',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор результата анализа',
    ),
    Column(
        'user_id',
        Integer,
        ForeignKey(
            'users.id',
            name='anlysis_user_id_fk',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment='Идентификатор пользователя',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        default=get_current_dt(TimeConstants.TIMEZONE),
        comment='Дата загрузки отзывов',
    ),
    Column(
        'source_type',
        String,
        nullable=False,
        comment='Тип источника (файл или сайт)',
    ),
    Column(
        'source_url',
        Text,
        nullable=False,
        comment='Ссылка на источник',
    ),
    Column(
        'entry_anlysis',
        ARRAY(JSONB),
        comment='Список результатов анализа по каждому отзыву',
    ),
    Column(
        'full_analysis',
        JSONB,
        comment='Общий результат анализа по всем отзывам',
    ),
    comment='Таблица, содержащая результаты анализа отзывов',
)

feedbacks = Table(
    'feedbacks',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор обратной связи',
    ),
    Column(
        'user_id',
        Integer,
        ForeignKey(
            'users.id',
            name='feedbacks_user_id_fk',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment='Идентификатор пользователя',
    ),
    Column(
        'dt',
        DateTime,
        nullable=False,
        default=get_current_dt(TimeConstants.TIMEZONE),
        comment='Дата отправки сообщения от пользователя',
    ),
    Column(
        'response_dt',
        DateTime,
        comment='Дата отправки сообщения от службы поддержки',
    ),
    Column(
        'message',
        Text,
        nullable=False,
        comment='Сообщение от пользователя',
    ),
    Column(
        'response',
        Text,
        comment='Ответ от службы поддержки',
    ),
    Column(
        'sender_email',
        String,
        nullable=False,
        comment='Email отправителя',
    ),
    Column(
        'recipient_email',
        String,
        nullable=False,
        comment='Email службы поддержки',
    ),
    comment='Таблица, содержащая информацию об обратной связи.',
)

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
