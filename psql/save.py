import psycopg2
import pandas as pd
import numpy as np
import logging

class PSQL():
    def __init__(self, db_name):
        self.conn = psycopg2.connect(db_name)
        self.cur = conn.cursor()

    def save_to_db(self, df):
        print('From psql.save.save_to_db')
        print(df)

    def close(self):
        self.conn.close()