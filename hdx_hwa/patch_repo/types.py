"""
Types that should be available outside of the patch_repo package
"""

from collections import namedtuple


Patch = namedtuple('Patch', ['patch_sequence_number', 'name', 'patch_path', 'commit_hash', 'permanent_download_url'])
