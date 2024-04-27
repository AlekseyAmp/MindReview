"""add_use_field_in_stopwords

Revision ID: 1aa63a5afded
Revises: 9bd84c01dec5
Create Date: 2024-04-26 19:29:52.071938+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1aa63a5afded'
down_revision: Union[str, None] = '9bd84c01dec5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'stopwords',
        sa.Column(
            'use',
            sa.Boolean(),
            nullable=False,
            comment='Использовать стоп-слово или нет'
        ),
        schema='data'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stopwords', 'use', schema='data')
    # ### end Alembic commands ###