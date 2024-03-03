"""unique raw name

Revision ID: 800e678f3912
Revises: d8501a2c6962
Create Date: 2024-03-03 14:34:27.421088+00:00

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '800e678f3912'
down_revision: Union[str, None] = 'd8501a2c6962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('raw_name', 'cities', ['raw_name'], schema='data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('raw_name', 'cities', schema='data', type_='unique')
    # ### end Alembic commands ###
