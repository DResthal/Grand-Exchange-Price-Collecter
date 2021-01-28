# Fetch items from groups in api
from apifetch.req_retry import ReqRetry
from apifetch.logger_setup import CustomLogger
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import sys
import json
import os

# base_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

error_log = logging.getLogger("e_log")
application_log = logging.getLogger("a_log")

retry_session = ReqRetry().retry_session()


def log_error(c_msg: str, err: str, url: str = "N/A", res: str = "N/A") -> None:
    custom_message = f"{c_msg}\n\n{err}"
    error_log.warning(custom_message)
    error_log.warning(f"Affected URL: {url}")
    error_log.warning(f"URL Response: {res}")


class FetchItems:
    def __init__(self):
        pass

    def fetch_item_json(url: str) -> dict:
        print(f"Fetching: {url}")
        try:
            item = retry_session.get(url).json()
            return item['items']
        except json.JSONDecodeError as e:
            log_error(f"JSON Error in fetch_item_json", e, url=url)
            print()
            pass
        except:
            log_error(f"Unknown Exception", sys.exc_info(), url=url)
            pass
