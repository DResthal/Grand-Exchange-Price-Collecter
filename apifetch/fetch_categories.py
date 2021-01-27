# Fetch groups from categories in api
from apifetch.req_retry import ReqRetry
from apifetch.logger_setup import CustomLogger
import requests as req
import apifetch.parse_groups
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging

today = datetime.now().strftime("%m-%d-%Y")
retry_session = ReqRetry().retry_session()

item_parser = apifetch.parse_groups.ItemParser()

### LOGGING ###
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

error_log = logging.getLogger("e_log")
application_log = logging.getLogger("a_log")


########################################################################################

def log_error(c_msg: str, err: str, url: str = "N/A", res: str = "N/A") -> None:
        custom_message = f"{c_msg}\n\n{err}"
        error_log.warning(custom_message)
        error_log.warning(f"Affected URL: {url}")
        error_log.warning(f"URL Response: {res}")

application_log.info(
    f'Begin fetching categories: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}'
)
print(f'Begin fetching categories: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')

categories_url = (
    "https://secure.runescape.com/m=itemdb_rs/api/catalogue/category.json?category="
)


def process_item_groups(cat_resp: list, cat_num: int) -> pd.DataFrame:
    group_list = []
    for group in cat_resp:
        # Skip if no items exist, wasted time
        if group["items"] == 0:
            application_log.info(f'Group {group["letter"]} has no items, pass.')
            print(f'Sanity Check: Group {group["letter"]} has no items, pass.')
            pass
        else:
            # Encode for url
            url_encoded_group = item_parser.url_encode(group)

            # Add number of pages
            with_num_pages = item_parser.add_num_of_pages(url_encoded_group)

            # Build urls for each page
            group_urls = []
            for p in range(with_num_pages["num_of_pages"]):
                group_urls.append(item_parser.build_url(with_num_pages, p + 1, cat_num))
                group.update({"urls": group_urls})
                group_list.append(group)

    group_list_dataframe = pd.DataFrame(group_list)
    return group_list_dataframe


def get_all_categories(n_cats: int=43) -> None:
    columns = ["letter", "items", "num_of_pages", "urls"]
    end_df = pd.DataFrame(columns=columns)
    for i in range(n_cats):
        print(f"Fetching Category {i}")
        try:
            # Returns a list of dicts
            current_url = categories_url + str(i)
            category_list = retry_session.get(current_url).json()["alpha"]
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
        urls = end_df["urls"].explode("urls")
        urls = urls.drop_duplicates()

    # Save all api urls to csv
    urls.to_csv("group_urls.csv")
    # Save all groups and their respective api urls to csv
    # end_df.to_csv("item_groups.csv")


application_log.info(f'Completed at: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
print(f'Completed at: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
