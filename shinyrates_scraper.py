"""
shinyrates_scraper.py

Scraper to collect data from shinyrates.com every minute.
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
        logger.debug(f"Wrote data for {last_updated}")


def stream_data():
    """Gather data from shinyrates.com every minute"""

    last_data = None
    while True:
        data = requests.get("https://shinyrates.com/data/rate").json()

        if data == last_data:
            logger.info("Still nothing")
            time.sleep(1)

        write_to_file(data, datetime.now().strftime("%Y%m%d_%H%M%S"))
        last_data = copy.deepcopy(data)
        logger.info("Sleeping")
        time.sleep(60)


if __name__ == "__main__":
    stream_data()
