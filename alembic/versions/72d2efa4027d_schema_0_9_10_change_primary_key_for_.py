"""schema 0.9.10 change primary key for funding_vat

Revision ID: 72d2efa4027d
Revises: 47ec461dd69b
Create Date: 2025-03-24 16:26:42.537949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72d2efa4027d'
down_revision: Union[str, None] = '47ec461dd69b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('funding_vat_pkey', 'funding_vat', type_='primary')
    op.create_primary_key('funding_vat_pkey', 'funding_vat', ['appeal_code', 'location_ref', 'reference_period_start'])


def downgrade() -> None:
    op.drop_constraint('funding_vat_pkey', 'funding_vat', type_='primary')
    op.create_primary_key('funding_vat_pkey', 'funding_vat', ['appeal_code', 'location_ref'])
