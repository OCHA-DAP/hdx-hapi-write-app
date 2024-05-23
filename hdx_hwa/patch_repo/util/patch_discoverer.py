import logging
from typing import Dict

from hdx_hwa.patch_repo.communication.api import (
    download_file_content_from_github,
    get_content_list_from_commit_folder,
    get_latest_commit_hash_and_date_on_branch,
)
from hdx_hwa.patch_repo.types import Patch

logger = logging.getLogger(__name__)


class PatchDiscoverer:
    def __init__(self, folder: str = None) -> None:
        self.folder = folder
        self.commit_hash, self.commit_date = get_latest_commit_hash_and_date_on_branch()
        self.raw_files = get_content_list_from_commit_folder(self.commit_hash, folder, True)
        self.hash_to_target_name_map: Dict[str, str] = {}
        self.target_name_to_patch_map: Dict[str, Patch] = {}

    def create_hash_to_target_name_map(self) -> Dict[str, str]:
        for file in self.raw_files:
            if file['name'].endswith('.hash'):
                content = download_file_content_from_github(file['download_url'])
                if content:
                    hash = content.strip().split(' ')[0]
                    # removing file extension and name endings from filename to remain with the target name
                    # for ex: operational_presence_view.hash -> operational_presence
                    key = file['name'].replace('.hash', '').replace('_view', '')
                    self.hash_to_target_name_map[key] = hash

    def create_target_name_to_patch_map(self) -> Dict[str, Patch]:
        for file in self.raw_files:
            if file['name'].endswith('.csv.gz'):
                # removing file extension and name endings from filename to remain with the target name
                # for ex: operational_presence_view.csv.gz -> operational_presence
                target = file['name'].replace('.gz', '').replace('.csv', '').replace('_view', '')
                patch = Patch(
                    patch_target=target,
                    patch_path=f'{self.folder}/{file["name"]}',
                    patch_permalink_url=file['download_url'],
                    patch_hash=self.hash_to_target_name_map[target],
                    commit_hash=self.commit_hash,
                    commit_date=self.commit_date,
                )
                self.target_name_to_patch_map[target] = patch
