import logging

from typing import List

from hdx_hwa.config.config import get_config
from hdx_hwa.patch_repo.types import Patch
from hdx_hwa.patch_repo.util.patch_discoverer import PatchDiscoverer

logger = logging.getLogger(__name__)

_CONFIG = get_config()


def discover_patches_from_repo() -> List[Patch]:
    logger.info('Discovering patches')
    patch_discoverer = PatchDiscoverer(_CONFIG.HWA_PATCH_FOLDER)
    patch_discoverer.create_hash_to_target_name_map()
    patch_discoverer.create_target_name_to_patch_map()
    return patch_discoverer.target_name_to_patch_map
