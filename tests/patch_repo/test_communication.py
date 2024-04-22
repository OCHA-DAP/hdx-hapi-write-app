from hdx_hwa.patch_repo.communication.api import get_content_list_from_commit_folder, get_latest_commit_on_branch


def test_get_latest_commit_on_branch(use_test_patch_discovery_branch):
    commit_hash = get_latest_commit_on_branch()
    assert len(commit_hash) in (40, 64)  # 40 for SHA-1, 64 for SHA-256
    assert commit_hash.isalnum()


def test_get_content_list_from_commit(use_test_patch_discovery_branch):
    commit_hash = get_latest_commit_on_branch()
    folder_results = get_content_list_from_commit_folder(commit_hash, '2023', only_files=False)
    assert len(folder_results) == 2
    assert set([r['name'] for r in folder_results]) == {'11', '12'}

    file_results = get_content_list_from_commit_folder(commit_hash, '2023/12', only_files=True)
    assert len(file_results) == 2
    assert set([r['name'] for r in file_results]) == {'hapi_patch_03_abc.json', 'hapi_patch_04_abc.json'}
