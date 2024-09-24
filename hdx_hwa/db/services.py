import logging

from datetime import datetime, timezone
from typing import Dict, List

from sqlalchemy import Table

from hapi_schema.db_patch import DBPatch, StateEnum
from hapi_schema.utils.base import Base

# we need this imports so that sqlAlchemy knows about them
from hapi_schema.db_views_as_tables import (
    DBLocationVAT,  # noqa
    DBAdmin1VAT,  # noqa
    DBAdmin2VAT,  # noqa
    DBConflictEventVAT,  # noqa
    DBDatasetVAT,  # noqa
    DBResourceVAT,  # noqa
    DBOrgTypeVAT,  # noqa
    DBOrgVAT,  # noqa
    DBSectorVAT,  # noqa
    DBOperationalPresenceVAT,  # noqa
    DBNationalRiskVAT,  # noqa
    DBPopulationVAT,  # noqa
    DBHumanitarianNeedsVAT,  # noqa
    DBPovertyRateVAT,  # noqa
    DBWfpCommodityVAT,  # noqa
    DBWfpMarketVAT,  # noqa
    DBCurrencyVAT,  # noqa
    DBFoodPriceVAT,  # noqa
    DBFoodSecurityVAT,  # noqa
    DBFundingVAT,  # noqa
    DBRefugeesVAT,  # noqa
    DBAvailabilityVAT,  # noqa
    DBIDPsVAT,  # noqa
    DBReturneesVAT,  # noqa
)

from hdx_hwa.db.dao.patch_dao import get_highest_sequence_number, get_last_executed_patch, insert_new_patch
from hdx_hwa.db.dao.vat_dao import delete_all_data_from_table, insert_data_in_table
from hdx_hwa.patch_repo.types import Patch


from hdx_hwa.db.session_util import db_session, end_session


logger = logging.getLogger(__name__)


def get_latest_executed_patch_hash_for_target_from_db(patch_target: str) -> str:
    session = db_session()
    patch = get_last_executed_patch(session, patch_target)
    if patch:
        return patch.patch_hash
    else:
        return None


def create_new_patch_in_db(discovered_patch: Patch, result: bool):
    session = db_session()
    seq_no = get_highest_sequence_number(session) or 0
    state = StateEnum.executed if result else StateEnum.failed
    current_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

    db_patch = DBPatch(
        patch_permalink_url=discovered_patch.patch_permalink_url,
        patch_hash=discovered_patch.patch_hash,
        patch_target=discovered_patch.patch_target,
        patch_path=discovered_patch.patch_path,
        patch_sequence_number=seq_no + 1,
        commit_hash=discovered_patch.commit_hash,
        commit_date=discovered_patch.commit_date,
        state=state,
        execution_date=current_timestamp,
    )
    insert_new_patch(db_patch, session)

    logger.info('Creating new patch in db')


def find_latest_sequence_number_from_db() -> int:
    logger.info('Finding latest sequence number')
    return -1


def get_sqlalchemy_table(table_name: str) -> Table:
    try:
        vat_table = f'{table_name}_vat'
        table: Table = Base.metadata.tables[vat_table]
        return table
    except KeyError:
        logger.error(f'Could not find table {table_name} in Base.metadata')

    return None


def get_columns_and_types_from_table(table: Table) -> Dict[str, str]:
    return {column.name: type(column.type).__name__ for column in table.columns}


def insert_batch_into_table(table: Table, batch: List[dict]):
    session = db_session()
    insert_data_in_table(table, batch, session)


def clean_table(table: Table):
    session = db_session()
    delete_all_data_from_table(table, session)


def commit_db_changes():
    db_session().commit()


def end_db_session():
    end_session()
