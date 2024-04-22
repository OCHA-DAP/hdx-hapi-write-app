import logging

from dataclasses import dataclass
from datetime import datetime

from hdx_hwa.config.config import Config


logger = logging.getLogger(__name__)


@dataclass
class CurrentState:
    last_sequence_number: int
    last_patch_date: datetime


def get_latest_executed_patch(config: Config) -> CurrentState:
    logger.info('Getting current status')
    return None


def create_or_update_patch(config: Config, discovered_patch):
    logger.info('Creating or updating patch')
    return None


def find_next_patch_to_execute():
    logger.info('Finding next patch to execute')
    return None
