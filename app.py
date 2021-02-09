# Remember "Category -> Groups -> Items"
from apifetch.fetch_categories import get_all_categories
from apifetch.logger_setup import CustomLogger
from apifetch.fetch_items import FetchItems
from datetime import datetime
# from pandarallel import pandarallel
import pandas as pd
import sys
import logging
import time
import os

error_log = CustomLogger("e_log", "error.log", level=logging.WARNING).create_logger()
application_log = CustomLogger("a_log", "app.log", level=logging.INFO).create_logger()

### Function Definitions ###


def log_error(c_msg: str, err: str, url: str = "N/A", res: str = "N/A") -> None:
    custom_message = f"{c_msg}\n\n{err}"
    error_log.warning(custom_message)
    error_log.warning(f"Affected URL: {url}")
    error_log.warning(f"URL Response: {res}")


def file_is_old(file_path: str, max_age: int = 604800) -> None:
    """max_age is in seconds

    minute = 60
    hour   = 3600
    12 hrs = 43200
    day    = 86400
    week   = 604800
    """
    x = os.stat(file_path)
    age = time.time() - x.st_mtime
    print(f"File {file_path} is {age} seconds old.")

    if age > max_age:
        application_log.info(f"File {file_path} is too old, generating new file.")
        return True
    else:
        application_log.info(
            f"File {file_path} is too new to replace, skipping file generation"
        )
        return False


def fetch_group_responses():
    pandarallel.initialize()
    fetcher = FetchItems()
    try:
        # temp = ser.parallel_apply(fetcher.fetch_item_json)
        temp = ser.apply(fetcher.fetch_item_json)
    except TypeError as e:
        print(e)
    except:
        e = sys.exc_info()
        print(e)


url_file_path = os.path.abspath("group_urls.csv")
group_url_response_file_path = os.path.abspath("group_url_responses.csv")


if not os.path.exists(url_file_path):
    application_log.info("groups_urls.csv not found, fetching urls")
    print("Fetching group url list")
    get_all_categories()
elif file_is_old(url_file_path):
    application_log.info("groups_urls.csv exists, checking age")
    get_all_categories()
else:
    application_log.info(
        "groups_urls.csv exists and is not old enough to update/replace. "
    )


try:
    idf = pd.read_csv("group_urls.csv")
    print(f'idf type: {type(idf)}')
    ser = idf['urls']
except:
    e = sys.exc_info()
    print(e)

# Check file exists
# Check age
# Generate file if none exists or too old.
if not os.path.exists(group_url_response_file_path):
    print("NO RESPONSE FILE EXISTS\n Generating new file... This WILL take a while!")
    fetch_group_responses()
elif file_is_old(group_url_response_file_path, 43200):
    fetch_group_responses()
else:
    pass

print(f'Application finished: {datetime.now().strftime("%m-%d-%Y_%H_%M_%S")}')
