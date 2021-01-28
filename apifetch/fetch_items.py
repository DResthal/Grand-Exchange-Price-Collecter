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

    def fetch_item_json(url: str, retries: int=3) -> pd.DataFrame:
        print(f"Fetching: {url}")
        try:
            items = retry_session.get(url).json()['items']
            item_list = []
            for i in items:
                item = {
                    'icon': i['icon'],
                    'icon_large': i['icon_large'],
                    'id': i['id'],
                    'type': i['type'],
                    'typeIcon': i['typeIcon'],
                    'name': i['name'],
                    'description': i['description'],
                    'current': i['current'],
                    'today': i['today'],
                    'members': i['members']
                }
                item_list.append(item)

            return(pd.Series(item_list))
                
                
            
        except json.JSONDecodeError as e:
            log_error(f"JSON Error in fetch_item_json", e, url=url)
            if retries < 3:
                time.wait(1)
                fetch_item_json(url)
            else:
                log_error(f"Unable to receive JSON response after 3 attempts", e, url=url, res=retry_session.get(url).content())
                pass
        except:
            log_error(f"Unknown Exception", sys.exc_info(), url=url)
            pass
