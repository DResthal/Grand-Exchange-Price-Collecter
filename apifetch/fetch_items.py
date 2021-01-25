# Fetch items from groups in api
from req_retry import ReqRetry
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

# base_url = "https://secure.runescape.com/m=itemdb_rs/api/catalogue/items.json?category=0&alpha=a&page=1"


retry_session = ReqRetry().retry_session()


class FetchItems:
    def __init__(self):
        pass

    def load_urls():
        df = pd.read_csv("group_urls.csv")
        return df

    def fetch_item_json(url):
        item = retry_session.get(url).json()
        return item
