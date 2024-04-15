from dataclasses import dataclass
import logging

from hdx_hwa.config.helper import create_pg_uri_from_env_without_protocol

logger = logging.getLogger(__name__)

@dataclass
class Config:
    # HAPI Database configuration
    SQL_ALCHEMY_PSYCOPG2_DB_URI: str

CONFIG = None


def get_config() -> Config:
    
    global CONFIG
    if not CONFIG:
        db_uri_without_protocol = create_pg_uri_from_env_without_protocol()
        sql_alchemy_psycopg2_db_uri = \
            f'postgresql+psycopg2://{db_uri_without_protocol}'
        
        CONFIG = Config(
            SQL_ALCHEMY_PSYCOPG2_DB_URI=sql_alchemy_psycopg2_db_uri,
        )

    return CONFIG
