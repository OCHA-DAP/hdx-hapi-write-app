from logging import Logger

from hapi_schema.db_age_range import DBAgeRange
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session


def test_sample(log: Logger, session_maker: sessionmaker[Session]):
    log.info('test_sample')
    session = session_maker()
    try:
        query = select(DBAgeRange)
        result = session.execute(query)
        assert len(result.scalars().all()) > 0
    except Exception as e:
        raise e
    finally:
        session.close()
