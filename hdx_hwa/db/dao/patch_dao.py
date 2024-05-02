import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select

from sqlalchemy import create_engine
from hdx_hwa.config.config import get_config


from hapi_schema.db_patch import DBPatch

logger = logging.getLogger(__name__)

# Functions to implement
# get patch by id - DONE
# create new patch
# update a patch
# find next patch to execute → failed or discovered patch with lowest sequence number
# find last executed patch → executed patch with highest sequence number


def get_patch_by_id(id: int, db: Session = None) -> list[DBPatch]:
    db = get_db_connection(db)
    query = select(DBPatch)
    query = query.where(DBPatch.id == id)
    result = db.execute(query)
    patch_data = result.scalars().all()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Retrieved {len(patch_data)} rows from the database')

    return patch_data


def get_highest_sequence_number(db: Session) -> int:
    db = get_db_connection(db)
    query = select(sqlalchemy.func.max(DBPatch.patch_sequence_number))
    result = db.execute(query)
    sequence_number = result.scalars().all()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {sequence_number} rows from the database')

    return sequence_number[0]


def get_db_connection(db: Session) -> Session:
    if db is None:
        engine = create_engine(
            get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
        )
        # print(get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI, flush=True)
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return db
