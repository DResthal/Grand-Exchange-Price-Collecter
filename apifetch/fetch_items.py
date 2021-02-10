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
from sqlalchemy import create_engine 
import psycopg2 

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


    def save_csv(self, df, filename):
        filename = f'{filename}_{self.now}.csv'
        if os.path.exists(filename):
            df.to_csv(filename, header=False, mode="a")
        else:
            df.to_csv(filename, header=True, mode="w")

    def convert_to_int(self, x):
        
        if type(x) = int:
            pass
        else:
            x = x.strip()
            x = x.replace(' ', '').replace(',', '')
            
            if "k" in x:
                lett = x[-1].upper()
                num = x[:-1]
                num = float(num)
                num = num * 10**3
            elif "m" in x:
                lett = x[-1].upper()
                num = x[:-1]
                num = float(num)
                num = num * 10**6
            elif "b" in x:
                lett = x[-1].upper()
                num = x[:-1]
                num = float(num)
                num = num * 10**9
            else:
                num = int(x)

            return(int(num))

        
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
                    'item_id'    : i['id'],
                    'icon'       : i['icon'],
                    'item_type'  : i['type'],
                    'name'       : i['name'],
                    'description': i['description'],
                    'is_members' : i['members']
                }

                price = {
                    'item_id'     : i['id'],
                    'price'       : str(i['current']['price']),
                    'trend'       : i['today']['trend'],
                    'change_today': i['today']['price']
                }

                items_list.append(item)
                price_list.append(price)

            item_df = pd.DataFrame(items_list)
            item_df = item_df.set_index('item_id')

            price_df = pd.DataFrame(price_list)
            price_df = price_df.set_index('item_id')
            # Convert K and M to 1000 and 1000000
            price_df["price"] = price_df.price.apply(self.convert_to_int)
            price_df["change_today"] = price_df.change_today.apply(self.convert_to_int)

            self.save_csv(item_df, 'items')
            self.save_csv(price_df, 'prices')
            
            '''
            engine = create_engine('postgresql://username:password@localhost:5432/grandexchange')
            item_df.to_sql('item', con=engine, if_exists='append')
            price_df.to_sql('price', con=engine, if_exists='append')
            '''
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
              
