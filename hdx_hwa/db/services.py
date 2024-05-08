import logging

from hdx_hwa.patch_repo.types import Patch


logger = logging.getLogger(__name__)


def get_latest_executed_patch_for_target_from_db():
    logger.info('Getting current status')
    return None


def create_new_patch_in_db(discovered_patch: Patch, result: bool, seq_number: int):
    logger.info('Creating new patch in db')


def find_latest_sequence_number_from_db() -> int:
    logger.info('Finding latest sequence number')
    return -1
