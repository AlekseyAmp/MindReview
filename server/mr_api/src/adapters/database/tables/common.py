from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, JSONB

from src.adapters.database.settings import settings
from src.application.constants import (
    SourceType,
    Status,
    TimeConstants,
    UserRole,
)
from src.application.utils import get_current_dt

metadata = MetaData(schema=settings.SCHEMAS["common"])

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
        default=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
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
        ENUM(
            *[user_role.value for user_role in UserRole],
            name='user_role_enum',
        ),
        nullable=False,
        default=UserRole.USER.value,
        comment='Роль пользователя',
    ),
    Column(
        'is_premium',
        Boolean,
        default=False,
        comment='Есть подписка или нет',
    ),
    comment='Таблица, содержащая информацию о пользователях',
)

analyze = Table(
    'analyze',
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
            'common.users.id',
            name='common.analyze_user_id_fk',
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
        default=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
        comment='Дата загрузки отзывов',
    ),
    Column(
        'source_type',
        ENUM(
            *[source_type.value for source_type in SourceType],
            name='source_type_enum',
        ),
        nullable=False,
        comment='Тип источника (тест, файл или сайт)',
    ),
    Column(
        'source_url',
        Text,
        comment='Ссылка на источник',
    ),
    Column(
        'entries_analyze',
        ARRAY(JSONB),
        comment='Список результатов анализа по каждому отзыву',
    ),
    Column(
        'full_analyze',
        JSONB,
        comment='Общий результат анализа по всем отзывам',
    ),
    Column(
        'status',
        ENUM(
            *[status.value for status in Status],
            name='status_enum',
        ),
        comment='Статус анализа (выполнен, ошибка)',
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
            'common.users.id',
            name='common.feedbacks_user_id_fk',
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
        default=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
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
