
from hdx_hwa.config.config import get_config
from hdx_hwa.db.services import create_or_update_patch, find_next_patch_to_execute, get_current_status
from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches


def process():
    config = get_config()
    current_status = get_current_status(config)

    list_of_patches = discover_patches(config, current_status)
    if list_of_patches:
        for discovered_patch in list_of_patches:
            create_or_update_patch(config, discovered_patch)
        
    while patch_metadata := find_next_patch_to_execute():
        execute_patch(config, patch_metadata)
    