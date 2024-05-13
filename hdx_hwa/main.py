import logging

from hdx_hwa.db.services import end_db_session, get_latest_executed_patch_hash_for_target_from_db

from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches_from_repo

logger = logging.getLogger(__name__)


def process():
    list_of_patches = discover_patches_from_repo()
    if list_of_patches:
        for discovered_patch in list_of_patches.values():
            # Below part happens in a single db transaction
            try:
                patch_hash = get_latest_executed_patch_hash_for_target_from_db(discovered_patch.patch_target)
                if patch_hash != discovered_patch.patch_hash:
                    logger.info(
                        f'Loading patch data for {discovered_patch.patch_target} '
                        f'and commit hash {discovered_patch.commit_hash}'
                    )
                    execute_patch(discovered_patch)
                else:
                    logger.info(
                        f'Patch data for {discovered_patch.patch_target} is already loaded. '
                        f'Commit hash: {discovered_patch.commit_hash}'
                    )
            except Exception as e:
                logger.error(f'Error while processing patch for target: {discovered_patch.patch_target}: {str(e)}')
            finally:
                end_db_session()
