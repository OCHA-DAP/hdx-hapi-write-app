"""migrate schema from 0.9.11 to 0.9.13

Revision ID: 18ec0e988794
Revises: 0a84c302c248
Create Date: 2025-04-02 09:19:46.809303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18ec0e988794'
down_revision: Union[str, None] = '0a84c302c248'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
