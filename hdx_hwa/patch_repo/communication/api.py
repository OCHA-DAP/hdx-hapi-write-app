import requests

from datetime import datetime, timezone
from typing import Dict, List, Tuple
from dateutil.parser import parse as dateutil_parse
from hdx_hwa.config.config import get_config


CONFIG = get_config()


def _get_api_headers() -> Dict:
    return {
        'Authorization': f'Bearer {CONFIG.HWA_PATCH_TOKEN}',
        'Content-Type': 'application/json',
    }


def get_latest_commit_hash_and_date_on_branch() -> Tuple[str, datetime]:
    url = f'{CONFIG.HWA_PATCH_REPO_URL}/branches/{CONFIG.HWA_PATCH_BRANCH_NAME}'
    headers = _get_api_headers()
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    timestamp = dateutil_parse(data['commit']['commit']['committer']['date'])
    if timestamp.tzinfo:
        timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)
    latest_commit_hash = data['commit']['sha']
    return latest_commit_hash, timestamp


def get_content_list_from_commit_folder(commit_hash: str, folder: str, only_files: bool) -> List[Dict]:
    """Get list of files OR folders (never both) in a specific folder at a specific commit hash

    Args:
        commit_hash (str): Commit hash
        folder (str): Folder to search in
        only_files (bool): If True, only files are returned. If False, only folders are returned
    Returns:
        list: List of found files or folders
    """
    url = f'{CONFIG.HWA_PATCH_REPO_URL}/contents/{folder}?ref={commit_hash}'
    headers = _get_api_headers()
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    type = 'file' if only_files else 'dir'

    return [c for c in data if c['type'] == type]


def download_file_content_from_github(url: str) -> str:
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    return response.text.strip()
