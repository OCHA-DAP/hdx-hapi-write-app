import logging
from sqlalchemy.orm import sessionmaker, Session
from hdx_hwa.db.dao.patch_dao import get_patch_by_id, get_highest_sequence_number


def test_get_patch_by_id(log: logging.Logger, session_maker: sessionmaker[Session]):
    session = session_maker()
    result = get_patch_by_id(1, db=session)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].commit_hash == '66e7e589a1224a1832ba7360817dda7a7d9313cf'


def test_get_highest_sequence_number(log: logging.Logger, session_maker: sessionmaker[Session]):
    session = session_maker()
    result = get_highest_sequence_number(db=session)

    assert result == 3
