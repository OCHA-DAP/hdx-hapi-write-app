from io import BytesIO
from typing import Generator, List

import requests
import logging
import gzip
import csv

logger = logging.getLogger(__name__)


def read_rows_from_patch_repo(url: str) -> Generator[List, None, None]:
    response = requests.get(url)
    response.raise_for_status()

    with gzip.open(BytesIO(response.content), 'rt') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            # logger.info(row)
            yield row
