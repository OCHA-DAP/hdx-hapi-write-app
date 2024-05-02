import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select

from sqlalchemy import create_engine
from hdx_hwa.config.config import get_config


from hapi_schema.db_patch import DBPatch, StateEnum

logger = logging.getLogger(__name__)

# Functions to implement
# get patch by id - DONE
# create new patch
# update a patch
# find next patch to execute → failed or discovered patch with lowest sequence number
# find last executed patch → executed patch with highest sequence number


def get_patch_by_id(id: int, db: Session = None) -> DBPatch:
    db = get_db_connection(db)
    query = select(DBPatch)
    query = query.where(DBPatch.id == id)
    result = db.execute(query)
    patch_data = result.scalars().all()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Retrieved {len(patch_data)} rows from the database')

    return patch_data[0]


def get_highest_sequence_number(db: Session) -> int:
    db = get_db_connection(db)
    query = select(sqlalchemy.func.max(DBPatch.patch_sequence_number))
    result = db.execute(query)
    sequence_number = result.scalars().all()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {sequence_number} rows from the database')

    return sequence_number[0]


def get_most_recent_patch(db: Session) -> DBPatch:
    db = get_db_connection(db)
    query = select(DBPatch).order_by(DBPatch.execution_date.desc()).where(DBPatch.execution_date.is_not(None))
    result = db.execute(query).scalars().all()
    most_recent = result[0]

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {most_recent} rows from the database')

    return most_recent


def get_next_patch_to_execute(db: Session) -> DBPatch:
    db = get_db_connection(db)
    query = (
        select(DBPatch)
        .order_by(DBPatch.patch_sequence_number.asc())
        .where(DBPatch.state == StateEnum.discovered or DBPatch.state == StateEnum.failed)
    )
    result = db.execute(query).scalars().all()
    most_recent = None
    if result is not None and len(result) == 1:
        most_recent = result[0]

    print(f'Executing SQL query: {query}', flush=True)
    print(f'Got result {most_recent} rows from the database', flush=True)

    return most_recent


def insert_new_patch(patch: DBPatch, db: Session) -> str:
    status = 'success'

    try:
        db.add(patch)
        db.commit()
        db.close()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        status = 'failure: wrong type'
    except sqlalchemy.exc.IntegrityError:
        status = 'failure: integrity error'

    return status


def get_db_connection(db: Session) -> Session:
    if db is None:
        engine = create_engine(
            get_config().SQL_ALCHEMY_PSYCOPG2_DB_URI,
        )
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return db
