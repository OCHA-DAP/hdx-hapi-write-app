"""migrate schema from 0.9.17 to 0.9.18 patching

Revision ID: 1ea928a90784
Revises: 2ee49c67b525
Create Date: 2026-10-02 13:14:31.806222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ea928a90784'
down_revision: Union[str, None] = '2ee49c67b525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('resource_vat', 'is_hxl')

def downgrade() -> None:
    # A NOT NULL column re-added to a non-empty table needs a default; the original values are lost.
    # The default stays so a rolled-back HWA 0.2.6 can still load patches that no longer have is_hxl.
    op.add_column('resource_vat', sa.Column('is_hxl', sa.Boolean(), nullable=False, server_default=sa.false()))

