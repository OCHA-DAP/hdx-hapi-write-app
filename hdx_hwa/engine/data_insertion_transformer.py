from datetime import datetime
from typing import Any, Dict, List

# for postgres: numeric and decimal are synonims
NUMERIC_TYPES = {'Integer', 'Decimal', 'Numeric'}


class DataInsertionTransformer:
    """
    A class that prepares a row of data to be inserted into the database
    """

    def __init__(self, table_col_to_type: Dict[str, str], csv_columns: List[str]) -> None:
        self.table_col_to_type = table_col_to_type
        self.csv_column_name_to_index = {col: i for i, col in enumerate(csv_columns)}

    def _transform_string_to_datetime(self, value: str) -> datetime:
        value = value.strip()
        if value:
            return value
        else:
            return None

    def _transform_string_to_type(self, value: str, type: str) -> Any:
        result = value
        if type == 'Boolean':
            if value == 'f':
                result = False
            elif value == 't':
                result = True
            else:
                result = None
        elif type == 'DateTime':
            result = self._transform_string_to_datetime(value)
        elif type in NUMERIC_TYPES:
            if len(value) == 0:
                result = None  # Empty string should be treated as NULL for integer columns

        return result

    def _compute_value(self, column_name: str, csv_row: List[str]) -> Any:
        value = csv_row[self.csv_column_name_to_index[column_name]]
        typed_value = self._transform_string_to_type(value, self.table_col_to_type[column_name])
        return typed_value

    def row_to_dict(self, csv_row: List[str]) -> Dict[str, Any]:
        """
        Given a row of data from a CSV file, return a dictionary that maps the table column names to the corresponding
        values in the row.
        """
        return {
            col: self._compute_value(col, csv_row)
            for col in self.table_col_to_type.keys()
            if col in self.csv_column_name_to_index
        }
