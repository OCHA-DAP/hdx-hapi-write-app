import logging

from hdx_hwa.config.config import Config


logger = logging.getLogger(__name__)


def execute_patch(config: Config, patch_metadata) -> bool:
    logger.info('Executing patch')
    return False



