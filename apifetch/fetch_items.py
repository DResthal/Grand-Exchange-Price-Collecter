# Fetch items from groups in api
from apifetch.req_retry import ReqRetry
from apifetch.logger_setup import CustomLogger
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import sys
import traceback
import json
import os

# base_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"

error_log = logging.getLogger("e_log")
application_log = logging.getLogger("a_log")

retry_session = ReqRetry().retry_session()

def log_error(c_msg: str, *err: str, url: str = "N/A", res: str = "N/A") -> None:
    custom_message = f"{c_msg}\n{err}"
    error_log.warning(custom_message)
    error_log.warning(f"Affected URL: {url}")
    error_log.warning(f"URL Response: {res}\n\n\n")


class FetchItems:
    def __init__(self):
        self.now = datetime.now().strftime("%m-%d-%Y-%H")
        self.file_name = f'all_items_{self.now}.csv'
        self.file_path = os.path.abspath(self.file_name)

    def save_items_to_csv(self, df: pd.DataFrame) -> None:
        if os.path.exists(self.file_path):
            df.to_csv(self.file_name, header=False, mode='a')
        else:
            df.to_csv(self.file_name, header=True, mode='a')

    def fetch_item_json(self, url: str, n_tries: int=3) -> pd.DataFrame:
        print(f"Fetching: {url}")
        try:
            res = retry_session.get(url)
            res.encoding = 'ISO-8859-1'
            items = res.json()['items']
            items = json.loads(json.dumps(items))
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
            
            df = pd.DataFrame(item_list)
            df = df.set_index('id')
            self.save_items_to_csv(df)
            
            
        # This needs to be broken out, however previous except blocks here failed repeatedly
        # So I am condensing for now, logging errors and will break out as errors appear
        except:
            res_text = ''
            if res.text:
                res_text = f'{str(res.headers)}\nTEXT: {str(res.text)}\n'
            if res.content:
                res_text = f'{str(res.headers)}\nCONTENT: {str(res.content)}\n'
            log_error('unknown error in item url resolution...', sys.exc_info(), url=url, res=res_text)
            pass
              