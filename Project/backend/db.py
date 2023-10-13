import sqlite3
import alpaca
from datetime import timedelta
from datetime import datetime
import time
import pandas as pd
import random

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

            self.cursor.execute("INSERT INTO databaseapp_stock VALUES (?, ?, ?, ?, ?)", (random.randint(0, 9223372036854775808), ticker, row["close"], unix_time, "0"))
        
        self.conn.commit()

    def __clear_data(self, ticker):
        self.cursor.execute(f"DELETE FROM databaseapp_stock WHERE stock_ticker = '{ticker}'")
        self.conn.commit()

    def clear_prediction(self, ticker=None): # UNTESTED

        if ticker is None:
            self.cursor.execute("DELETE FROM databaseapp_stock WHERE stock_prediction = 'true'")
        else:
            self.cursor.execute(f"DELETE FROM databaseapp_stock WHERE stock_ticker = '{ticker}' AND stock_prediction = '1'")

    def update(self, ticker, start, end=None):
        if end is None:
            end = datetime.now().date() - timedelta(days = 1)

        self.__clear_data(ticker)
        self.__add_data(ticker, start, end)

    def test(self):
        # self.__clear_data("AAPL")
        self.__add_data("GOOGL", "2023-01-01")
        


ses = session("storage.db")

# ses.update("AAPL", "2022-01-01")

ses.test()