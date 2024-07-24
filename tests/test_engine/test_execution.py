from datetime import datetime

from hapi_schema.db_patch import DBPatch
from hapi_schema.db_views_as_tables import DBNationalRiskVAT
from sqlalchemy import delete, func, select
from hdx_hwa.db.dao.patch_dao import get_highest_sequence_number

# from hdx_hwa.db.temp.db_operational_presence_vat import DBOperationalPresenceVAT
from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.types import Patch


def test_execute_patch(use_test_patch_discovery_branch, db_session):
    db_session.execute(delete(DBPatch))
    patch = Patch(
        patch_permalink_url='https://github.com/OCHA-DAP/hapi-pipelines-prod/raw/4614653ff2b6a79c47defd13dea9e28027550175/database/csv/national_risk_view.csv.gz',
        patch_target='national_risk',
        patch_path='national_risk_view.csv.gz',
        patch_hash='abcd1234',
        commit_date=datetime(2024, 5, 2, 10, 31, 11),
        commit_hash='9dd5e045113d3e4ccacc7ba06336d2b3a6d26333',
    )
    execute_patch(patch, row_limit=2000)

    query = select(func.count(DBNationalRiskVAT.resource_hdx_id))
    count_op_rows = db_session.execute(query).scalar()
    assert count_op_rows > 0 and count_op_rows <= 2000

    assert get_highest_sequence_number(db_session) == 1
    pass
