import sqlite3
import alpaca
from datetime import timedelta
from datetime import datetime
import time
import pandas as pd
import random
from config import database as config

class session:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        self.alp = alpaca.session()

    def __add_data(self, ticker, start, end=None): # add the data for a ticker to the database
        if end is None: # if no end date is specified, use yesterday
            datetime.now().date() - timedelta(days = 1)

        data = self.alp.get_history(ticker, "1D", start, end, filter="close")

        for index, row in data.iterrows(): # iterate through the data and add it to the database

            time_obj = pd.to_datetime(row["time"], unit="s")
            unix_time = time_obj.timestamp()

            # This is awful and painful but I have no better solution so it will persist until soom*tm*
            self.cursor.execute(f"INSERT INTO {config.table_name} ({config.id_column_name}, {config.ticker_column_name}, {config.price_column_name}, {config.date_column_name}, {config.prediction_column_name}) VALUES (?, ?, ?, ?, ?)", (random.randint(0, 9223372036854775808), ticker, row["close"], unix_time, "0"))
        
        self.conn.commit()

    def clear_data(self, ticker):
        self.cursor.execute(f"DELETE FROM {config.table_name} WHERE {config.ticker_column_name} = '{ticker}'")
        self.conn.commit()

    def clear_prediction(self, ticker=None): # UNTESTED

        if ticker is None:
            self.cursor.execute(f"DELETE FROM {config.table_name} WHERE {config.prediction_column_name} = 'true'")
        else:
            self.cursor.execute(f"DELETE FROM {config.table_name} WHERE {config.ticker_column_name} = '{ticker}' AND {config.prediction_column_name} = '1'")

    def update(self, ticker, start, end=None):
        if end is None:
            end = datetime.now().date() - timedelta(days = 1)

        self.clear_data(ticker)
        self.__add_data(ticker, start, end)