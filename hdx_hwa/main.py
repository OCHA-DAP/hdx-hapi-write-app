import logging

from hdx_hwa.db.services import end_db_session, get_latest_executed_patch_hash_for_target_from_db

from hdx_hwa.engine.services import execute_patch
from hdx_hwa.patch_repo.services import discover_patches_from_repo
from hdx_hwa.util.slack_wrapper import SlackClientWrapper
from hdx_hwa.util.timer import Timer

logger = logging.getLogger(__name__)


def process():
    slack_wrapper = SlackClientWrapper()
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
                    # logger.info(
                    #     f'Loading patch data for {discovered_patch.patch_target} '
                    #     f'and commit hash {discovered_patch.commit_hash}'
                    # )
                    import_proces_timer.next(
                        f'Loading data for {discovered_patch.patch_target} '
                        f'and commit hash {discovered_patch.commit_hash}'
                    )
                    execute_patch(discovered_patch)
                    finished_loading_message = f'Finished loading data for *{discovered_patch.patch_target}* ' \
                        f'from {discovered_patch.patch_permalink_url} ' \
                        f'and commit hash {discovered_patch.commit_hash}'
                    import_proces_timer.next(finished_loading_message)
                    slack_wrapper.post_to_slack_channel(finished_loading_message)
                    # logger.info(
                    #     f'Finished loading data for {discovered_patch.patch_target} '
                    #     f'and commit hash {discovered_patch.commit_hash}'
                    # )
                else:
                    logger.info(
                        f'Patch data for {discovered_patch.patch_target} is already loaded. '
                        f'Commit hash: {discovered_patch.commit_hash}'
                    )
            except Exception as e:
                message = f'Error while processing patch for target: *{discovered_patch.patch_target}*: ' \
                    f'from {discovered_patch.patch_permalink_url} ' \
                    f'{str(e)}'
                logger.error(message)
                slack_wrapper.post_to_slack_channel(message)
            finally:
                end_db_session()

    process_finished_message = 'Finished import process'
    import_proces_timer.next(process_finished_message)
    slack_wrapper.post_to_slack_channel(process_finished_message)
