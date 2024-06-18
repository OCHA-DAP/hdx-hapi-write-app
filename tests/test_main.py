import unittest.mock as mock

from hdx_hwa.main import process
from hdx_hwa.main import SlackClientWrapper
from hdx_hwa.patch_repo.types import Patch


TARGET = 'sector'
COMMIT_HASH = '123456'

DISCOVERED_PATCHES = {
    TARGET: Patch(
        patch_target=TARGET,
        patch_path='database/csv/sector_view.csv.gz',
        patch_permalink_url='',
        patch_hash='abcdefg',
        commit_hash=COMMIT_HASH,
        commit_date=None,
    )
}

LATEST_PATCH_HASH_NEW = None
LATEST_PATCH_HASH_EXISTING = 'abcdefg'


@mock.patch.object(SlackClientWrapper, 'post_to_slack_channel')
@mock.patch('hdx_hwa.main.execute_patch')
@mock.patch('hdx_hwa.main.get_latest_executed_patch_hash_for_target_from_db', return_value=LATEST_PATCH_HASH_NEW)
@mock.patch('hdx_hwa.main.discover_patches_from_repo', return_value=DISCOVERED_PATCHES)
def test_main_new_patch(discover_patches_mock, get_latest_hash_mock, execute_patch_mock, post_to_slack_mock):
    process()
    assert post_to_slack_mock.call_count == 2
    assert post_to_slack_mock.call_args_list[0].args[0] == \
        f'Finished loading data for {TARGET} and commit hash {COMMIT_HASH}'
    assert post_to_slack_mock.call_args_list[1].args[0] == 'Finished import process'


@mock.patch.object(SlackClientWrapper, 'post_to_slack_channel')
@mock.patch('hdx_hwa.main.get_latest_executed_patch_hash_for_target_from_db', return_value=LATEST_PATCH_HASH_EXISTING)
@mock.patch('hdx_hwa.main.discover_patches_from_repo', return_value=DISCOVERED_PATCHES)
def test_main_existing_patch(discover_patches_mock, get_latest_hash_mock, post_to_slack_mock):
    process()
    assert post_to_slack_mock.call_count == 1
    assert post_to_slack_mock.call_args_list[0].args[0] == 'Finished import process'