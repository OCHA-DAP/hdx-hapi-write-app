import logging
import os

from dataclasses import dataclass
from typing import Optional

from hdx_hwa.config.helper import create_pg_uri_from_env_without_protocol

logger = logging.getLogger(__name__)


@dataclass
class Config:
    # HAPI Database configuration
    SQL_ALCHEMY_PSYCOPG2_DB_URI: str
    HWA_PATCH_REPO_URL: str
    HWA_PATCH_BRANCH_NAME: str
    HWA_PATCH_FOLDER: str
    HWA_PATCH_TOKEN: Optional[str]
    HWA_SLACK_NOTIFICATION_CHANNEL: str
    HAPI_SLACK_CENTRE_ACCESS_TOKEN: Optional[str]


CONFIG = None


def get_config() -> Config:
    global CONFIG
    if not CONFIG:
        db_uri_without_protocol = create_pg_uri_from_env_without_protocol()
        sql_alchemy_psycopg2_db_uri = f'postgresql+psycopg2://{db_uri_without_protocol}'

        CONFIG = Config(
            SQL_ALCHEMY_PSYCOPG2_DB_URI=sql_alchemy_psycopg2_db_uri,
            HWA_PATCH_REPO_URL=os.getenv(
                'HWA_PATCH_REPO_URL', 'https://api.github.com/repos/OCHA-DAP/hdx-hapi-write-app-patches'
            ),
            HWA_PATCH_BRANCH_NAME=os.getenv('HWA_PATCH_BRANCH_NAME', 'db-export'),
            HWA_PATCH_TOKEN=os.getenv('HWA_PATCH_TOKEN', None),
            HWA_PATCH_FOLDER=os.getenv('HWA_PATCH_FOLDER', 'database/csv'),
            HWA_SLACK_NOTIFICATION_CHANNEL=
                os.getenv('HWA_SLACK_NOTIFICATION_CHANNEL', 'topic-hapi-testing-notifications'),
            HAPI_SLACK_CENTRE_ACCESS_TOKEN=os.getenv('HAPI_SLACK_CENTRE_ACCESS_TOKEN', None),
        )

    return CONFIG
