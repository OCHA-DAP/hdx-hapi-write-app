"""Migrate schema from 0.8.16 to 0.8.17

Revision ID: 2762198a212d
Revises: ecca1ef814df
Create Date: 2024-09-20 07:39:29.866577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2762198a212d'
down_revision: Union[str, None] = 'ecca1ef814df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('idps_vat', sa.Column('operation', sa.String(), nullable=False))
    op.alter_column('idps_vat', 'reporting_round',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('idps_vat_pkey', 'idps_vat', type_='primary')
    op.create_primary_key('idps_vat_pkey', 'idps_vat', ['admin2_ref','assessment_type',
                                                        'reporting_round','operation','reference_period_start'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('idps_vat', 'reporting_round',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('idps_vat', 'operation')
    op.drop_constraint('idps_vat_pkey', 'idps_vat', type_='primary')
    op.create_primary_key('idps_vat_pkey', 'idps_vat', ['admin2_ref','assessment_type'])
    # ### end Alembic commands ###
