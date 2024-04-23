import logging
import os
from typing import List

import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from hdx_hwa.config.config import get_config

from hapi_schema.utils.base import Base


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


@pytest.fixture(scope='function')
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


@pytest.fixture(scope='function')
def populate_test_data(log: logging.Logger, session_maker: sessionmaker[Session]):
    log.info('Populating with test data')
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    Base.metadata.create_all(engine)
    db_session = session_maker()

    try:
        with open(SAMPLE_DATA_SQL_FILE, 'r') as file:
            sql_commands = file.read()
            db_session.execute(text(sql_commands))
            db_session.commit()
            log.info('Test data inserted successfully')
    except Exception as e:
        log.error(f'Error while inserting test data: {str(e).splitlines()[0]}')
        db_session.rollback()
        raise e
    finally:
        db_session.close()


@pytest.fixture(scope='function', autouse=True)
def refresh_db(clear_db_tables, populate_test_data):
    pass
