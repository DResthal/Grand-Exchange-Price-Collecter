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


    def fetch_item_json(self, url: str, n_tries: int=3) -> pd.DataFrame:
        application_log.info(f'Fetching: {url}')

        try:
            res = retry_session.get(url)
            res.encoding = 'ISO-8859-1'
            items = res.json()['items']
            # Validates JSON but returns in dict form and not string
            items = json.loads(json.dumps(items))

            items_list = []
            price_list = []

            for i in items:

                item = {
                    'ItemID'     : i['id'],
                    'Icon'       : i['icon'],
                    'Type'       : i['type'],
                    'Name'       : i['name'],
                    'Description': i['description'],
                    'IsMembers'  : i['members']
                }

                price = {
                    'ItemID'     : i['id'],
                    'Price'      : i['current']['price'],
                    'Trend'      : i['today']['trend'],
                    'ChangeToday': i['today']['price']
                }

                items_list.append(item)
                price_list.append(price)

            item_df = pd.DataFrame(items_list)
            item_df = item_df.set_index('ItemID')

            price_df = pd.DataFrame(price_list)
            price_df = price_df.set_index('ItemID')
            

            item_df.to_csv('Items.csv', header=False, mode='a')
            price_df.to_csv('Prices.csv', header=False, mode='a')

            print('fetch_item_json Completed!')
            
            '''
            Old way of saving all items to the csv
            I now, instead, want to save items to a database table "Items" (no overwrites)
            and save prices to a table "Price" including today's date

            df = pd.DataFrame(item_list)
            if df.columns.values.any():
                df = df.set_index('id')
                self.save_items_to_csv(df)
            else:
                pass
            '''
            
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
              