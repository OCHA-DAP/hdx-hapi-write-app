from logging import Logger

from hapi_schema.db_age_range import DBAgeRange
from sqlalchemy import select
from sqlalchemy.orm import Session


def test_sample(log: Logger, db_session: Session):
    log.info('test_sample')
    try:
        query = select(DBAgeRange)
        result = db_session.execute(query)
        assert len(result.scalars().all()) > 0
    except Exception as e:
        raise e
