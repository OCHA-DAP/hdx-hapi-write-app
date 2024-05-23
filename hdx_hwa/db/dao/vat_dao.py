import logging

from typing import Any, Dict, List
from sqlalchemy import Table, insert
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


def insert_data_in_table(table: Table, row_list: List[Dict[str, Any]], session: Session):
    session.execute(insert(table), row_list)


def delete_all_data_from_table(table: Table, session: Session):
    session.execute(table.delete())