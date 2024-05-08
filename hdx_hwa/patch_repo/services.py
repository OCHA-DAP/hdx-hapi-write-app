import logging

from typing import List

from hdx_hwa.patch_repo.types import Patch
from hdx_hwa.patch_repo.util.patch_discoverer import PatchDiscoverer

logger = logging.getLogger(__name__)


def discover_patches(last_sequence_number: int, last_path: str) -> List[Patch]:
    logger.info('Discovering patches')
    path_list = last_path.split('/')
    if len(path_list) == 2:
        year = int(path_list[0])
        month = int(path_list[1])

        patch_discoverer_current_year = PatchDiscoverer(year, month, last_sequence_number)
        discovered_patches = patch_discoverer_current_year.find_patches()

        patch_discoverer_next_year = PatchDiscoverer(
            year + 1, 1, last_sequence_number, commit_hash=patch_discoverer_current_year.commit_hash
        )
        discovered_patches += patch_discoverer_next_year.find_patches()
        return discovered_patches
    else:
        logger.error(f'Invalid path: {last_path}')
        raise ValueError(f'Invalid path: {last_path}')
