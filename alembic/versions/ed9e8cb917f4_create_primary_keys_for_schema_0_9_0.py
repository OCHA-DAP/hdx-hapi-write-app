"""Create primary keys for schema 0.9.0

Revision ID: ed9e8cb917f4
Revises: 0d68c20a0946
Create Date: 2024-10-18 12:48:19.277369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed9e8cb917f4'
down_revision: Union[str, None] = '0d68c20a0946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PRIMARY_KEYS = {
        "conflict_event_vat": [
        "admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "event_type",
        "reference_period_start",
    ],
    # "food_price_vat":[], food_price inherits provider names from wfp_market
    "food_security_vat": ["admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "ipc_type",
        "ipc_phase",
        "reference_period_start"],
    "humanitarian_needs_vat": ["admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "gender",
        "age_range",
        "sector_code",
        "population_group",
        "population_status",
        "disabled_marker",
        "reference_period_start",],
    "idps_vat": ["admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "assessment_type",
        "reporting_round",
        "operation",
        "reference_period_start",],
    "operational_presence_vat":["admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "org_acronym",
        "org_name",
        "sector_code",
        "reference_period_start",],
    "population_vat": ["admin2_ref",
        "provider_admin1_name",
        "provider_admin2_name",
        "gender",
        "age_range",
        "reference_period_start",],
    "poverty_rate_vat": ["admin1_ref",
        "provider_admin1_name",
        "reference_period_start",],
    # "wpf_market_vat": [] - the primary key for wfp_market_vat is just ["code"] and hasn't changed
    }


def upgrade() -> None:
    for table_name, primary_keys in PRIMARY_KEYS.items():
        op.create_primary_key(f'{table_name}_pkey', table_name, primary_keys)


def downgrade() -> None:
    for table_name, _ in PRIMARY_KEYS.items():
        op.drop_constraint(f'{table_name}_pkey', table_name, type_='primary')
