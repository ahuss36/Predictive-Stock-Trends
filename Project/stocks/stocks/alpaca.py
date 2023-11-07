import alpaca_trade_api as tradeapi
from datetime import datetime
from datetime import timedelta
import pandas as pd

class session:

    ALPACA_API_KEY = "PKNA5BRTUQNYGT6HKOKU" # These have zero damage potential, so I am not worried about them being public
    ALPACA_SECRET_KEY = "UW2YAU3T6J0meNvwiNQbcqxwtYWu5anHxoe0AVgu"
    BASE_URL = "https://paper-api.alpaca.markets"

    def __init__(self):
        self.api = tradeapi.REST(self.ALPACA_API_KEY, self.ALPACA_SECRET_KEY, self.BASE_URL, api_version='v2')
    
    def get_account(self):
        return self.api.get_account()
    
    def get_position(self, symbol):
        return self.api.get_position(symbol)
    
    def get_positions(self):
        raw = self.api.list_positions()

        df = pd.DataFrame()
        
        df["symbol"] = [position.symbol for position in raw]
        df["qty"] = [position.qty for position in raw]
        df["price"] = [position.current_price for position in raw]
        df["market_value"] = [position.market_value for position in raw]

        return df
    
    def get_position(self, symbol):
        all = self.get_positions()

        return all.loc[all["symbol"] == symbol]

    # get_history('AAPL', '1D', '2020-01-01', '2020-01-10'), end date is optional
    def get_history(self, symbol, timeframe, start, end = datetime.now().date() - timedelta(days = 1), filter = None):

        data = self.api.get_bars(symbol, timeframe, start, end)

        df = pd.DataFrame()

        df["time"] = [bar.t for bar in data] # only take required elements from the dataframe
        df["open"] = [bar.o for bar in data]
        df["high"] = [bar.h for bar in data]
        df["low"] = [bar.l for bar in data]
        df["close"] = [bar.c for bar in data]
        df["volume"] = [bar.v for bar in data]

        if (filter != None): # if a filter is specified, filter the new dataframe
            newFilter = ["time", filter]
            df = df.filter(newFilter)

        return df
    
    def buy(self, symbol, qty, returnErrors = False):
        try:
            order = self.api.submit_order(symbol, qty, "buy", "market", "day") # submit the order
        except tradeapi.rest.APIError as e:
            if (returnErrors): # if the user wants to see the error, return it
                return e
            else:
                return []

        output = [order.symbol, order.qty, order.status]

        return output
    
    def sell(self, symbol, qty, returnErrors = False):
        try:
            order = self.api.submit_order(symbol, qty, "sell", "market", "day")
        except tradeapi.rest.APIError as e:
            if (returnErrors):
                return e
            else:
                return []


        output = [order.symbol, order.qty, order.filled_qty, order.filled_avg_price, order.status]

        return output

    def get_orders(self):
        order = self.api.list_orders()
    
        df = pd.DataFrame()

        df["symbol"] = [order.symbol for order in order]
        df["qty"] = [order.qty for order in order]
        df["filled_qty"] = [order.filled_qty for order in order]
        df["filled_avg_price"] = [order.filled_avg_price for order in order]
        df["status"] = [order.status for order in order]

        return df