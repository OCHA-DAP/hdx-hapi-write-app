from hdx_hwa.config.config import get_config
from hdx_hwa.db.services import create_or_update_patch, find_next_patch_to_execute, get_latest_executed_patch
from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches


def process():
    config = get_config()
    latest_executed_patch = get_latest_executed_patch(config)

    if latest_executed_patch:
        list_of_patches = discover_patches(
            latest_executed_patch.patch_sequence_number, latest_executed_patch.patch_path
        )
    else:
        list_of_patches = None
    if list_of_patches:
        for discovered_patch in list_of_patches:
            create_or_update_patch(config, discovered_patch)

    while patch_metadata := find_next_patch_to_execute():
        execute_patch(config, patch_metadata)
