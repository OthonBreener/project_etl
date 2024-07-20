"""alter table Data, include primary key and remove primary key in signal_id

Revision ID: 67c2165e8aaf
Revises: 60dc9aa821c8
Create Date: 2024-07-20 10:45:43.562057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67c2165e8aaf'
down_revision: Union[str, None] = '60dc9aa821c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'data',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            autoincrement=True,
            primary_key=True,
        ),
    )
    op.drop_constraint(
        'data_pkey', 'data', type_='primary'
    )
    op.create_primary_key(
        'data_pkey', 'data', ['id']
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'id')
    op.drop_constraint(
        'data_pkey', 'data', type_='primary'
    )
    op.create_primary_key(
        'data_pkey', 'data', ['signal_id']
    )
    # ### end Alembic commands ###
