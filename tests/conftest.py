import logging
import os
from typing import List

import pytest

from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import sessionmaker, Session


from hapi_schema.utils.base import Base
from hapi_schema.db_age_range import DBAgeRange
from hapi_schema.db_patch import DBPatch

from .sample_data.data_age_range import data_age_range
from .sample_data.data_patch import data_patch

from hdx_hwa.config.config import get_config

SAMPLE_DATA_SQL_FILE = 'tests/data/sample_data.sql'


def pytest_sessionstart(session):
    os.environ['HAPI_DB_NAME'] = 'hwa_test'


@pytest.fixture(scope='session')
def log():
    return logging.getLogger(__name__)


@pytest.fixture(scope='session')
def session_maker() -> sessionmaker[Session]:
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


@pytest.fixture(scope='session')
def list_of_db_tables(log: logging.Logger, session_maker: sessionmaker[Session]) -> List[str]:
    # log.info('Getting list of db tables')
    session = session_maker()
    try:
        result = session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        return [row[0] for row in result if row != 'alembic_version']
    except Exception as e:
        raise e
    finally:
        session.close()


@pytest.fixture(scope='session')
def clear_db_tables(log: logging.Logger, session_maker: sessionmaker[Session], list_of_db_tables: List[str]):
    log.info('Clearing database')
    db_session = session_maker()
    try:
        for table in list_of_db_tables:
            db_session.execute(text(f'TRUNCATE TABLE {table} CASCADE;'))
        db_session.commit()
    except Exception as e:
        log.error(f'Error while clearing test data: {str(e).splitlines()[0]}')
        db_session.rollback()
        raise e
    finally:
        db_session.close()


@pytest.fixture(scope='session')
def populate_test_data(log: logging.Logger, session_maker: sessionmaker[Session]):
    log.info('Populating with test data')
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    Base.metadata.create_all(engine)
    db_session = session_maker()

    db_session.execute(insert(DBAgeRange), data_age_range)
    db_session.execute(insert(DBPatch), data_patch)

    db_session.commit()


@pytest.fixture(scope='session', autouse=True)
def refresh_db(clear_db_tables, populate_test_data):
    pass
