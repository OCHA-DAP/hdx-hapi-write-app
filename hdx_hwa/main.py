from hdx_hwa.config.config import get_config
from hdx_hwa.db.services import (
    get_latest_executed_patch_for_target_from_db,
    find_latest_sequence_number_from_db,
    create_new_patch_in_db,
)
from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches_from_repo


def process():
    config = get_config()
    list_of_patches = discover_patches_from_repo()
    if list_of_patches:
        for discovered_patch in list_of_patches:
            # Below part should probably be run in a single db transaction
            patch = get_latest_executed_patch_for_target_from_db(discovered_patch.patch_target)
            if patch.patch_hash != discovered_patch.patch_hash:
                result = execute_patch(config, discovered_patch)
                seq_number = find_latest_sequence_number_from_db() + 1
                create_new_patch_in_db(discovered_patch, result, seq_number)
