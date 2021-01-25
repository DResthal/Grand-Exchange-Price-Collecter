# Get items from groups in api
from req_retry import ReqRetry
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

retry_session = ReqRetry().retry_session()


def load_urls():
    df = pd.read_csv("group_urls.csv")
    return df


def get_items_json(url):
    item = retry_session.get(url).json()
    return item
