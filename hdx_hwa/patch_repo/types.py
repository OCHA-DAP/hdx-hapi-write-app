"""
Types that should be available outside of the patch_repo package
"""

from collections import namedtuple


Patch = namedtuple(
    'Patch', ['patch_permalink_url', 'patch_target', 'patch_path', 'patch_hash', 'commit_date', 'commit_hash']
)
