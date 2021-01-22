import requests as req
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import parse_items
import math
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import sys

today = datetime.now().strftime("%m-%d-%Y")

### LOGGING ###
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


error_log = setup_logger("e_log", "error.log", level=logging.WARNING)
application_log = setup_logger("a_log", "app.log", level=logging.INFO)


def log_error(c_msg, err, url="N/A", res="N/A"):
    custom_message = f"{c_msg}\n\n{err}"
    error_log.warning(custom_message)
    error_log.warning(f"Affected URL: {url}")
    error_log.warning(f"URL Response: {res}")


### Requests retry setup ###

# Create a session, attempt to connect, retry if failed and return if passed
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):

    session = session or req.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


########################################################################################

application_log.info(
    f'Starting data scrape: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}'
)
print(f'Starting data scrape: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')

categories_url = (
    "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category="
)
items_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"


def process_item_groups(cat_resp, cat_num):
    group_list = []
    for group in cat_resp:
        # Encode for url
        url_encoded_group = parse_items.url_encode(group)
        # Add number of pages
        with_num_pages = parse_items.add_num_of_pages(url_encoded_group)

        # Build urls for each page
        group_urls = []
        if with_num_pages["num_of_pages"] != 0:
            for p in range(with_num_pages["num_of_pages"]):
                group_urls.append(parse_items.build_url(with_num_pages, p + 1, cat_num))
        else:
            pass

        group.update({"urls": group_urls})
        group_list.append(group)

    group_list_dataframe = pd.DataFrame(group_list)
    return group_list_dataframe


### Main Loop (42) ###
# Empty df for appending all groups
columns = ['letter', 'items', 'num_of_pages', 'urls']
end_df = pd.DataFrame(columns=columns)

for i in range(42):
    print(f"Fetching Category {i}")
    try:
        # Returns a list of dicts
        current_url = categories_url + str(i)
        category_list = req.get(current_url).json()["alpha"]
        application_log.info(f"Category {i}: \n{category_list}")
    except req.exceptions.Timeout as e:
        log_error("Request timeout", e, current_url)
        pass
    except req.exceptions.TooManyRedirects as e:
        log_error("Too Many Redirects, check URL", e, current_url)
        pass
    except json.decoder.JSONDecodeError as e:
        log_error("JSON Decode error", e, current_url, req.get(current_url).content)
    except req.exceptions.RequestException as e:
        log_error("Unknown Exception", e, current_url)
        pass

    df = process_item_groups(category_list, i)
    df = df.replace(0, np.nan).dropna()
    end_df = pd.concat([end_df, df], sort=False)

end_df.to_csv('item_groups.csv')

application_log.info(f'Completed at: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
print(f'Completed at: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
