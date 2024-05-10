import datetime
import logging
import sqlalchemy
from sqlalchemy.orm import Session

from hapi_schema.db_patch import StateEnum, DBPatch
from hdx_hwa.db.dao.patch_dao import (
    get_patch_by_id,
    get_highest_sequence_number,
    get_most_recent_patch,
    insert_new_patch,
    get_next_patch_to_execute,
    get_last_executed_patch,
)


def test_get_highest_sequence_number(log: logging.Logger, db_session: Session):
    result = get_highest_sequence_number(db=db_session)

    assert result == 3


def test_get_most_recent_patch(log: logging.Logger, db_session: Session):
    result = get_most_recent_patch(db=db_session)

    assert result.state == StateEnum.failed
    assert result.execution_date == datetime.datetime(2023, 1, 3, 0, 0)


def test_insert_new_patch_failure_type(log: logging.Logger, db_session: Session):
    status = insert_new_patch(1, db=db_session)

    assert status == 'failure: wrong type'


def test_insert_new_patch_failure_integrity(log: logging.Logger, db_session: Session):
    new_patch = DBPatch()
    try:
        insert_new_patch(new_patch, db=db_session)
        db_session.commit()
        assert False
    except sqlalchemy.exc.IntegrityError:
        assert True


def test_insert_new_patch_success(log: logging.Logger, db_session: Session):
    new_patch = DBPatch(
        patch_sequence_number=4,
        commit_hash='554f18a92cf6a23a14e0f29356a6dec150f651gg',
        commit_date=datetime.datetime(2023, 1, 4),
        patch_path='2024/01/hapi_patch_4_hno.json',
        patch_target='humanitarian_needs',
        patch_hash='554f18a92cf6a23a14e0f29356a6dec150f651hh',
        patch_permalink_url='https://github.com/OCHA-DAP/hapi-patch-repo/blob/554f18a92cf6a23a14e0f29356a6dec150f651ff/2024/01/hapi_patch_4_hno.json',
        state=StateEnum.discovered,
    )
    status = insert_new_patch(new_patch, db=db_session)
    db_session.commit()
    inserted_id = new_patch.id

    assert status == 'success'
    result = get_highest_sequence_number(db=db_session)
    assert result == 4

    result = get_patch_by_id(inserted_id, db=db_session)
    assert result.commit_hash == '554f18a92cf6a23a14e0f29356a6dec150f651gg'


def test_get_next_patch_to_execute(log: logging.Logger, db_session: Session):
    result = get_next_patch_to_execute(db=db_session)

    assert result.patch_sequence_number == 2
    assert result.state == StateEnum.failed


def test_get_last_executed_patch(log: logging.Logger, db_session: Session):
    result = get_last_executed_patch(db=db_session)

    assert result.patch_sequence_number == 1
    assert result.state == StateEnum.executed
