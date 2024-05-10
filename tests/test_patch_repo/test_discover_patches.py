from hdx_hwa.patch_repo.services import discover_patches_from_repo


def test_discover_patches(use_test_patch_discovery_branch):
    patches = discover_patches_from_repo()
    assert len(patches) == 3
    assert set(p.patch_target for p in patches.values()) == {
        'location_view',
        'national_risk_view',
        'operational_presence_view',
    }
