import logging
from typing import Dict, List

from hdx_hwa.db.services import (
    clean_table,
    commit_db_changes,
    create_new_patch_in_db,
    get_columns_and_types_from_table,
    get_sqlalchemy_table,
    insert_batch_into_table,
)
from hdx_hwa.engine.data_insertion_transformer import DataInsertionTransformer
from hdx_hwa.patch_repo.types import Patch
from hdx_hwa.patch_repo.util.csv_reader import read_rows_from_patch_repo

logger = logging.getLogger(__name__)

_BATCH = 10_000


def execute_patch(patch_metadata: Patch, row_limit: int = None):
    table = get_sqlalchemy_table(patch_metadata.patch_target)
    if table is not None:
        clean_table(table)
        column_to_type: str = get_columns_and_types_from_table(table)
        csv_row_generator = read_rows_from_patch_repo(patch_metadata.patch_permalink_url)
        header_row = next(csv_row_generator)
        transformer = DataInsertionTransformer(column_to_type, header_row)

        batch: List[Dict] = []
        for i, row in enumerate(csv_row_generator):
            if row_limit and i >= row_limit:
                break
            row_dict = transformer.row_to_dict(row)
            batch.append(row_dict)
            if len(batch) == _BATCH:
                insert_batch_into_table(table, batch)
                logger.info(f'Inserted {(i+1)/1000}k rows into {patch_metadata.patch_target}')
                batch = []

        # Insert the remaining rows
        if len(batch) > 0:
            insert_batch_into_table(table, batch)

        create_new_patch_in_db(patch_metadata, True)
        logger.info(f'Before committing {patch_metadata.patch_target}')
        commit_db_changes()
