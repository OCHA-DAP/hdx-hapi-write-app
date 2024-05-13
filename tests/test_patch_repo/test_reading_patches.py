import logging
from hdx_hwa.patch_repo.services import discover_patches_from_repo
from hdx_hwa.patch_repo.util.csv_reader import read_rows_from_patch_repo


logger = logging.getLogger(__name__)


def test_reading_patches(use_test_patch_discovery_branch):
    patches = discover_patches_from_repo()
    op_url = patches['operational_presence'].patch_permalink_url

    assert 'operational_presence' in op_url

    for i, row in enumerate(read_rows_from_patch_repo(op_url)):
        if i > 10:
            break
        logger.info(row)
    assert True
