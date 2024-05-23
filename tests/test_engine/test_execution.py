from datetime import datetime

from hapi_schema.db_patch import DBPatch
from sqlalchemy import delete, func, select
from hdx_hwa.db.dao.patch_dao import get_highest_sequence_number
from hdx_hwa.db.temp.db_operational_presence_vat import DBOperationalPresenceVAT
from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.types import Patch


def test_execute_patch(use_test_patch_discovery_branch, db_session):
    db_session.execute(delete(DBPatch))
    patch = Patch(
        patch_permalink_url='https://raw.githubusercontent.com/alexandru-m-g/test-hdx-hapi-write-app-patches/9dd5e045113d3e4ccacc7ba06336d2b3a6d26333/database/csv/operational_presence_view.csv.gz',
        patch_target='operational_presence',
        patch_path='database/csv/operational_presence_view.csv.gz',
        patch_hash='fa6286902e8caed163757871e1c82fc2',
        commit_date=datetime(2024, 5, 2, 10, 31, 11),
        commit_hash='9dd5e045113d3e4ccacc7ba06336d2b3a6d26333',
    )
    execute_patch(patch, row_limit=2000)

    query = select(func.count(DBOperationalPresenceVAT.resource_hdx_id))
    count_op_rows = db_session.execute(query).scalar()
    assert count_op_rows == 2000

    assert get_highest_sequence_number(db_session) == 1
