import logging

from hdx_hwa.db.services import end_db_session, get_latest_executed_patch_hash_for_target_from_db

from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches_from_repo
from hdx_hwa.util.timer import Timer

logger = logging.getLogger(__name__)


def process():
    import_proces_timer = Timer('Import timer', in_millis=False)
    list_of_patches = discover_patches_from_repo()
    if list_of_patches:
        for discovered_patch in list_of_patches.values():
            if discovered_patch.patch_target in ['patch']:
                continue
            # Below part happens in a single db transaction
            try:
                patch_hash = get_latest_executed_patch_hash_for_target_from_db(discovered_patch.patch_target)
                if patch_hash != discovered_patch.patch_hash:
                    logger.info(
                        f'Loading patch data for {discovered_patch.patch_target} '
                        f'and commit hash {discovered_patch.commit_hash}'
                    )
                    import_proces_timer.next(f'Started loading data for {discovered_patch.patch_target}')
                    execute_patch(discovered_patch)
                    import_proces_timer.next(f'Finished loading data for {discovered_patch.patch_target}')
                    logger.info(
                        f'Finished loading data for {discovered_patch.patch_target} '
                        f'and commit hash {discovered_patch.commit_hash}'
                    )
                else:
                    logger.info(
                        f'Patch data for {discovered_patch.patch_target} is already loaded. '
                        f'Commit hash: {discovered_patch.commit_hash}'
                    )
            except Exception as e:
                logger.error(f'Error while processing patch for target: {discovered_patch.patch_target}: {str(e)}')
            finally:
                end_db_session()

    import_proces_timer.next('Finished import process')
