from hdx_hwa.patch_repo.services import discover_patches


def test_discover_patches(use_test_patch_discovery_branch):
    patches = discover_patches(0, '2023/01')
    assert len(patches) == 7
    for i, p in enumerate(patches):
        assert p.patch_sequence_number == i + 1

    patches = discover_patches(4, '2023/12')
    assert len(patches) == 3
    for i, p in enumerate(patches):
        assert p.patch_sequence_number == i + 5
