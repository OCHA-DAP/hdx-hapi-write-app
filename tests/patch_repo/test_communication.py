from datetime import datetime

from hdx_hwa.patch_repo.communication.api import (
    get_content_list_from_commit_folder,
    get_latest_commit_hash_and_date_on_branch,
)


def test_get_latest_commit_hash_and_date_on_branch(use_test_patch_discovery_branch):
    commit_hash, commit_date = get_latest_commit_hash_and_date_on_branch()
    assert len(commit_hash) in (40, 64)  # 40 for SHA-1, 64 for SHA-256
    assert commit_hash.isalnum()
    assert datetime.now() > commit_date


def test_get_content_list_from_commit(use_test_patch_discovery_branch):
    commit_hash, _ = get_latest_commit_hash_and_date_on_branch()
    folder_results = get_content_list_from_commit_folder(commit_hash, 'database', only_files=False)
    assert len(folder_results) == 1
    assert set([r['name'] for r in folder_results]) == {'csv'}

    file_results = get_content_list_from_commit_folder(commit_hash, 'database/csv', only_files=True)
    assert len(file_results) == 6
    assert set([r['name'] for r in file_results]) == {
        'location_view.csv.gz',
        'location_view.hash',
        'national_risk_view.csv.gz',
        'national_risk_view.hash',
        'operational_presence_view.csv.gz',
        'operational_presence_view.hash',
    }
