import datetime
import logging
from sqlalchemy.orm import sessionmaker, Session

from hapi_schema.db_patch import StateEnum
from hdx_hwa.db.dao.patch_dao import (
    get_patch_by_id,
    get_highest_sequence_number,
    get_most_recent_patch,
    insert_new_patch,
)


def test_get_patch_by_id(log: logging.Logger, session_maker: sessionmaker[Session]):
    session = session_maker()
    result = get_patch_by_id(1, db=session)

    assert len(result) == 1
    assert result.id == 1
    assert result.commit_hash == '66e7e589a1224a1832ba7360817dda7a7d9313cf'


def test_get_highest_sequence_number(log: logging.Logger, session_maker: sessionmaker[Session]):
    session = session_maker()
    result = get_highest_sequence_number(db=session)

    assert result == 3


def test_get_most_recent_patch(log: logging.Logger, session_maker: sessionmaker[Session]):
    session = session_maker()
    result = get_most_recent_patch(db=session)

    assert result.state == StateEnum.failed
    assert result.execution_date == datetime.datetime(2023, 1, 3, 0, 0)
