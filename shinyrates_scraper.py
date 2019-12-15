"""
shinyrates_scraper.py

Scraper to collect data from shinyrates.com.
"""

import copy
import json
import time
import requests

from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from loguru import logger


def write_to_file(data: Dict[Any, Any], last_updated: int) -> None:
    """Write response data to an output file."""

    outdir = Path("data")
    if not outdir.exists():
        outdir.mkdir()

    with open(outdir.joinpath(f"{last_updated}.json"), "w") as f:
        json.dump(data, f, indent=4)
        logger.info(f"Wrote data for {last_updated}")


def stream_data():
    """
    Gather data from shinyrates.com whenever it updates

    The website claims to update every minute, but that's clearly not the case based on
    observations; it had the same data from at least 8:46 AM - 9:55 AM. Sleep for 5
    minutes and query every minute to see if we ever get different data.
    """

    last_data = None
    while True:
        data = requests.get("https://shinyrates.com/data/rate").json()

        if data == last_data:
            logger.debug("Still nothing")
            time.sleep(60)
            continue

        write_to_file(data, datetime.now().strftime("%Y%m%d_%H%M%S"))
        last_data = copy.deepcopy(data)
        logger.debug("Sleeping")
        time.sleep(300)


if __name__ == "__main__":
    stream_data()
