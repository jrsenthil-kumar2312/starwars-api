import requests
import petl as etl

from petl.util.base import Table
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


def fetch_data_from_url(fetch_url: str) -> dict | None:
    """Fetch data from the provided resource url."""

    response = requests.get(fetch_url)

    if response.status_code == 200:
        return response.json()

    logger.info(f"Failed to fetch data from {fetch_url}")
    return None
