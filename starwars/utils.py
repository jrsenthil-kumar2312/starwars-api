import logging

import petl as etl
from petl.util.base import Table

import requests

logger = logging.getLogger(__name__)


def fetch_data_from_url(fetch_url: str) -> dict | None:
    """Fetch data from the provided resource url."""

    response = requests.get(fetch_url)

    if response.status_code == 200:
        return response.json()

    logger.info(f"Failed to fetch data from {fetch_url}")
    return None

def remove_unused_columns(table_to_remove: Table, columns_to_remove: list) -> Table:
    """Removed unused columns from a table."""

    for column in columns_to_remove:
        if column in table_to_remove.header():
            table_to_remove = etl.cutout(table_to_remove, column)

    return table_to_remove
