from typing import Dict, List
import requests

from hdx_hwa.config.config import get_config


CONFIG = get_config()


def _get_api_headers() -> Dict:
    return {
        'Authorization': f'Bearer {CONFIG.HWA_PATCH_TOKEN}',
        'Content-Type': 'application/json',
    }


def get_latest_commit_on_branch() -> str:
    url = f'{CONFIG.HWA_PATCH_REPO_URL}/branches/{CONFIG.HWA_PATCH_BRANCH_NAME}'
    headers = _get_api_headers()
    response: requests.Response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    latest_commit_hash = data['commit']['sha']
    return latest_commit_hash


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

    response_list = []

    type = 'file' if only_files else 'dir'
    # content_list = data['files']
    for content in data:
        if content['type'] == type:
            response_list.append(
                {
                    'name': content['name'],
                    'patch_path': content['path'],
                    'permanent_download_url': content['download_url'],
                    'size': content['size'],
                }
            )
    return response_list
