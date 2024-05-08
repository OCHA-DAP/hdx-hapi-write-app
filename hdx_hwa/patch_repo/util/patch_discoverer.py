import logging
from typing import Dict, List

import requests

from hdx_hwa.patch_repo.communication.api import get_content_list_from_commit_folder, get_latest_commit_on_branch
from hdx_hwa.patch_repo.types import Patch

logger = logging.getLogger(__name__)


class PatchDiscoverer:
    def __init__(self, year: int, start_month: int, last_sequence_number: int, commit_hash: str = None) -> None:
        self.year = year
        self.start_month = start_month
        self.last_sequence_number = last_sequence_number
        self.commit_hash = commit_hash if commit_hash else get_latest_commit_on_branch()

        self.available_months_this_year: List[int] = None
        self.discovered_patches: List[Patch] = []

    def find_patches(self) -> List[Patch]:
        self.available_months_this_year = self._discover_available_months_for_year()
        for month in self.available_months_this_year:
            available_patches = self._discover_available_patches_for_year_and_month(month)
            self.discovered_patches.extend(available_patches)
        return self.discovered_patches

    def _discover_available_months_for_year(self) -> List[str]:
        logger.info(f'Discovering available months for year: {self.year}')
        filtered_months = []
        folders_in_year: List[Dict] = []
        try:
            folders_in_year = get_content_list_from_commit_folder(self.commit_hash, f'{self.year}', False)
        except requests.HTTPError as e:
            logger.warning(f'Error while discovering available months: {e}')
            if e.response.status_code != 404:
                # not expecting this error, re-raising exception
                raise e

        for folder_dict in folders_in_year:
            try:
                folder = folder_dict['name']
                month = int(folder)
                if month >= self.start_month:
                    filtered_months.append(folder)
            except ValueError:
                logger.warning(f'Skipping invalid month: {folder}')
        return filtered_months

    def _discover_available_patches_for_year_and_month(self, month: int) -> List[Patch]:
        logger.info(f'Discovering available patches for year: {self.year} and month: {month}')
        files_in_month: List[Dict] = get_content_list_from_commit_folder(self.commit_hash, f'{self.year}/{month}', True)
        filtered_patches: List[Patch] = []
        for file_dict in files_in_month:
            file = file_dict['name']
            if file.startswith('hapi_patch') and file.endswith('.json'):
                try:
                    patch_sequence_number = int(file.split('_')[2])
                    if patch_sequence_number > self.last_sequence_number:
                        patch = Patch(
                            patch_sequence_number=patch_sequence_number,
                            name=file,
                            patch_path=file_dict['patch_path'],
                            commit_hash=self.commit_hash,
                            permanent_download_url=file_dict['permanent_download_url'],
                        )

                        filtered_patches.append(patch)
                except (ValueError, IndexError):
                    logger.warning(f'Skipping invalid patch: {file}')
            else:
                logger.warning(f'Skipping invalid patch: {file}')

        return filtered_patches
