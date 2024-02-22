"""add tables

Revision ID: 5351c68a168e
Revises:
Create Date: 2024-02-22 11:05:50.090011+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5351c68a168e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'logs',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            comment='Уникальный идентификатор лога'
        ),
        sa.Column(
            'dt',
            sa.DateTime(),
            nullable=False,
            comment='Метка времени лога'
        ),
        sa.Column(
            'level',
            sa.String(),
            nullable=False,
            comment='Уровень важности лога'
        ),
        sa.Column(
            'message',
            sa.Text(),
            nullable=False,
            comment='Сообщение лога'
        ),
        sa.PrimaryKeyConstraint('id'),
        comment='Таблица, содержащая логи приложения.'
    )
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            comment='Уникальный идентификатор пользователя'
        ),
        sa.Column(
            'dt',
            sa.DateTime(),
            nullable=False,
            comment='Дата регистрации пользователя'
        ),
        sa.Column(
            'first_name',
            sa.String(),
            nullable=False,
            comment='Имя пользователя'
        ),
        sa.Column(
            'last_name',
            sa.String(),
            nullable=False,
            comment='Фамилия пользователя'
        ),
        sa.Column(
            'email',
            sa.String(),
            nullable=False,
            comment='Адрес электронной почты пользователя'
        ),
        sa.Column(
            'password',
            sa.String(),
            nullable=False,
            comment='Пароль пользователя'
        ),
        sa.Column(
            'role',
            sa.String(),
            nullable=False,
            comment='Роль пользователя'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        comment='Таблица, содержащая информацию о пользователях')
    op.create_table(
        'analysis',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            comment='Уникальный идентификатор результата анализа'
        ),
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False,
            comment='Идентификатор пользователя'
        ),
        sa.Column(
            'dt',
            sa.DateTime(),
            nullable=False,
            comment='Дата загрузки отзывов'
        ),
        sa.Column(
            'source_type',
            sa.String(),
            nullable=False,
            comment='Тип источника (файл или сайт)'
        ),
        sa.Column(
            'source_url',
            sa.Text(),
            nullable=False,
            comment='Ссылка на источник'
        ),
        sa.Column(
            'entry_anlysis',
            postgresql.ARRAY(
                postgresql.JSONB(
                    astext_type=sa.Text())),
            nullable=True,
            comment='Список результатов анализа по каждому отзыву'
        ),
        sa.Column(
            'full_analysis',
            postgresql.JSONB(
                astext_type=sa.Text()),
            nullable=True,
            comment='Общий результат анализа по всем отзывам'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='anlysis_user_id_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        comment='Таблица, содержащая результаты анализа отзывов'
    )
    op.create_table(
        'feedbacks',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            comment='Уникальный идентификатор обратной связи'
        ),
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False,
            comment='Идентификатор пользователя'
        ),
        sa.Column(
            'dt',
            sa.DateTime(),
            nullable=False,
            comment='Дата отправки сообщения от пользователя'
        ),
        sa.Column(
            'response_dt',
            sa.DateTime(),
            nullable=True,
            comment='Дата отправки сообщения от службы поддержки'
        ),
        sa.Column(
            'message',
            sa.Text(),
            nullable=False,
            comment='Сообщение от пользователя'
        ),
        sa.Column(
            'response',
            sa.Text(),
            nullable=True,
            comment='Ответ от службы поддержки'
        ),
        sa.Column(
            'sender_email',
            sa.String(),
            nullable=False,
            comment='Email отправителя'
        ),
        sa.Column(
            'recipient_email',
            sa.String(),
            nullable=False,
            comment='Email службы поддержки'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='feedbacks_user_id_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        comment='Таблица, содержащая информацию об обратной связи.'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedbacks')
    op.drop_table('analysis')
    op.drop_table('users')
    op.drop_table('logs')
    # ### end Alembic commands ###
