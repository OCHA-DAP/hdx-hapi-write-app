import logging
import os
from typing import Generator, List

import pytest

from sqlalchemy import Engine, MetaData, create_engine, inspect, text, insert
from sqlalchemy.orm import Session

from hapi_schema.utils.base import Base

from hapi_schema.db_patch import DBPatch
from hapi_schema.db_sector import DBSector
from hapi_schema.db_views_as_tables import DBNationalRiskVAT, DBLocationVAT  # noqa

from hdx_hwa.db.session_util import db_session as util_db_session

from hdx_hwa.config.config import get_config


from tests.sample_data.data_sector import data_sector
from tests.sample_data.data_patch import data_patch

# SAMPLE_DATA_SQL_FILE = 'tests/data/sample_data.sql'


def pytest_sessionstart(session):
    os.environ['HAPI_DB_NAME'] = 'hwa_test'
    os.environ['HWA_PATCH_REPO_URL'] = 'https://api.github.com/repos/alexandru-m-g/test-hdx-hapi-write-app-patches'
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    _drop_tables_and_views(engine)
    _create_tables(engine)


def _drop_tables_and_views(engine: Engine):
    # drop views
    inspector = inspect(engine)
    views = inspector.get_view_names()
    with engine.connect() as conn:
        for view in views:
            conn.execute(text(f'DROP VIEW IF EXISTS {view}'))
            conn.commit()

    # drop tables
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)


def _create_tables(engine: Engine):
    Base.metadata.create_all(engine)


@pytest.fixture(scope='session')
def log():
    return logging.getLogger(__name__)


# @pytest.fixture(scope='session')
# def session_maker() -> sessionmaker[Session]:
#     return session_creator()


@pytest.fixture(scope='function')
def db_session() -> Generator[Session, None, None]:
    with util_db_session() as session:
        yield session
    # session.close()


@pytest.fixture(scope='function')
def list_of_db_tables(log: logging.Logger, db_session: Session) -> List[str]:
    # log.info('Getting list of db tables')
    try:
        result = db_session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        return [row[0] for row in result if row != 'alembic_version']
    except Exception as e:
        raise e


@pytest.fixture(scope='function')
def clear_db_tables(log: logging.Logger, db_session: Session, list_of_db_tables: List[str]):
    log.info('Clearing database')
    try:
        for table in list_of_db_tables:
            db_session.execute(text(f'TRUNCATE TABLE {table} CASCADE;'))
        db_session.commit()
    except Exception as e:
        log.error(f'Error while clearing test data: {str(e).splitlines()[0]}')
        db_session.rollback()
        raise e


@pytest.fixture(scope='function')
def populate_test_data(log: logging.Logger, db_session: Session):
    log.info('Populating with test data')
    engine = create_engine(
        get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
    )
    Base.metadata.create_all(engine)

    db_session.execute(insert(DBSector), data_sector)
    db_session.execute(insert(DBPatch), data_patch)

    db_session.commit()


@pytest.fixture(scope='function', autouse=True)
def refresh_db(clear_db_tables, populate_test_data):
    pass


@pytest.fixture(scope='function')
def use_test_patch_discovery_branch():
    original_value = get_config().HWA_PATCH_BRANCH_NAME
    get_config().HWA_PATCH_BRANCH_NAME = 'test-full-csv-patches'
    yield
    get_config().HWA_PATCH_BRANCH_NAME = original_value
