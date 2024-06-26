import logging
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select


from hapi_schema.db_patch import DBPatch, StateEnum

logger = logging.getLogger(__name__)


def get_patch_by_id(id: int, db: Session = None) -> DBPatch:
    query = select(DBPatch)
    query = query.where(DBPatch.id == id)
    result = db.execute(query)
    patch_data = result.scalars().all()

    if result is not None and len(patch_data) == 1:
        patch_data = patch_data[0]

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Retrieved {patch_data} from the database')

    return patch_data


def get_highest_sequence_number(db: Session) -> int:
    query = select(sqlalchemy.func.max(DBPatch.patch_sequence_number))
    result = db.execute(query)
    sequence_number = result.scalar()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {sequence_number} rows from the database')

    return sequence_number


def get_most_recent_patch(db: Session) -> DBPatch:
    query = select(DBPatch).order_by(DBPatch.execution_date.desc()).where(DBPatch.execution_date.is_not(None))
    result = db.execute(query).scalars().all()
    most_recent = None
    if result is not None:
        most_recent = result[0]

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {most_recent} rows from the database')

    return most_recent


def get_next_patch_to_execute(db: Session) -> DBPatch:
    query = (
        select(DBPatch)
        .order_by(DBPatch.patch_sequence_number.asc())
        .where(DBPatch.state == StateEnum.discovered or DBPatch.state == StateEnum.failed)
    )
    result = db.execute(query).scalars().all()
    most_recent = None
    if result is not None and len(result) == 1:
        most_recent = result[0]

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {most_recent} rows from the database')

    return most_recent


def get_last_executed_patch(db: Session, patch_target: str = None) -> DBPatch:
    query = select(DBPatch).order_by(DBPatch.execution_date.desc()).where(DBPatch.state == StateEnum.executed)
    if patch_target:
        query = query.where(DBPatch.patch_target == patch_target)
    result = db.execute(query).scalar()

    logger.debug(f'Executing SQL query: {query}')
    logger.info(f'Got result {result} rows from the database')

    return result


def insert_new_patch(patch: DBPatch, db: Session) -> str:
    status = 'success'
    try:
        db.add(patch)
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        status = 'failure: wrong type'

    return status
