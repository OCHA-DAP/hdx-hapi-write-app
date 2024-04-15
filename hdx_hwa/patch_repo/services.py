import logging

from typing import List

from hdx_hwa.config.config import Config
from hdx_hwa.db.services import CurrentState


logger = logging.getLogger(__name__)

def discover_patches(config: Config, current_state: CurrentState) -> List:
    logger.info('Discovering patches') 
    return None
