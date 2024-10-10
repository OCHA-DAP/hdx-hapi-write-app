"""Migrate schema from 0.8.17 to 0.9.0

Revision ID: 0d68c20a0946
Revises: 2762198a212d
Create Date: 2024-10-10 12:22:14.166124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d68c20a0946'
down_revision: Union[str, None] = '2762198a212d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conflict_event_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('conflict_event_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.add_column('food_price_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('food_price_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.create_index(op.f('ix_food_price_vat_provider_admin1_name'), 'food_price_vat', ['provider_admin1_name'], unique=False)
    op.create_index(op.f('ix_food_price_vat_provider_admin2_name'), 'food_price_vat', ['provider_admin2_name'], unique=False)
    op.add_column('food_security_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('food_security_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.add_column('humanitarian_needs_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('humanitarian_needs_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.add_column('idps_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('idps_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.add_column('operational_presence_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('operational_presence_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.add_column('population_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('population_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.drop_index('ix_population_vat_reference_period_start', table_name='population_vat')
    op.add_column('poverty_rate_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.drop_index('ix_poverty_rate_vat_admin1_name', table_name='poverty_rate_vat')
    op.add_column('wfp_market_vat', sa.Column('provider_admin1_name', sa.String(length=512), nullable=False))
    op.add_column('wfp_market_vat', sa.Column('provider_admin2_name', sa.String(length=512), nullable=False))
    op.create_index(op.f('ix_wfp_market_vat_provider_admin1_name'), 'wfp_market_vat', ['provider_admin1_name'], unique=False)
    op.create_index(op.f('ix_wfp_market_vat_provider_admin2_name'), 'wfp_market_vat', ['provider_admin2_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wfp_market_vat_provider_admin2_name'), table_name='wfp_market_vat')
    op.drop_index(op.f('ix_wfp_market_vat_provider_admin1_name'), table_name='wfp_market_vat')
    op.drop_column('wfp_market_vat', 'provider_admin2_name')
    op.drop_column('wfp_market_vat', 'provider_admin1_name')
    op.create_index('ix_poverty_rate_vat_admin1_name', 'poverty_rate_vat', ['admin1_name'], unique=False)
    op.drop_column('poverty_rate_vat', 'provider_admin1_name')
    op.create_index('ix_population_vat_reference_period_start', 'population_vat', ['reference_period_start'], unique=False)
    op.drop_column('population_vat', 'provider_admin2_name')
    op.drop_column('population_vat', 'provider_admin1_name')
    op.drop_column('operational_presence_vat', 'provider_admin2_name')
    op.drop_column('operational_presence_vat', 'provider_admin1_name')
    op.drop_column('idps_vat', 'provider_admin2_name')
    op.drop_column('idps_vat', 'provider_admin1_name')
    op.drop_column('humanitarian_needs_vat', 'provider_admin2_name')
    op.drop_column('humanitarian_needs_vat', 'provider_admin1_name')
    op.drop_column('food_security_vat', 'provider_admin2_name')
    op.drop_column('food_security_vat', 'provider_admin1_name')
    op.drop_index(op.f('ix_food_price_vat_provider_admin2_name'), table_name='food_price_vat')
    op.drop_index(op.f('ix_food_price_vat_provider_admin1_name'), table_name='food_price_vat')
    op.drop_column('food_price_vat', 'provider_admin2_name')
    op.drop_column('food_price_vat', 'provider_admin1_name')
    op.drop_column('conflict_event_vat', 'provider_admin2_name')
    op.drop_column('conflict_event_vat', 'provider_admin1_name')
    # ### end Alembic commands ###
