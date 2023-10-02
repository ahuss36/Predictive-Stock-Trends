import alpaca_trade_api as tradeapi
from datetime import datetime
from datetime import timedelta
import pandas as pd

class session:

    ALPACA_API_KEY = "PK4B928AJY8WOHKYXLFP" # These have zero damage potential, so I am not worried about them being public
    ALPACA_SECRET_KEY = "nZpB5btAryUDZSbC9YtLOHNKLlaTCabaCp4KV1jY"
    BASE_URL = "https://paper-api.alpaca.markets"

    def __init__(self):
        self.api = tradeapi.REST(self.ALPACA_API_KEY, self.ALPACA_SECRET_KEY, self.BASE_URL, api_version='v2')
    
    def get_account(self):
        return self.api.get_account()
    
    def get_position(self, symbol):
        return self.api.get_position(symbol)
    
    def get_history(self, symbol, timeframe, start, end = datetime.now().date() - timedelta(days = 1), *args, **kwargs):

        data = self.api.get_bars(symbol, timeframe, start, end)

        df = pd.DataFrame()

        df["time"] = [bar.t for bar in data]
        df["open"] = [bar.o for bar in data]
        df["high"] = [bar.h for bar in data]
        df["low"] = [bar.l for bar in data]
        df["close"] = [bar.c for bar in data]
        df["volume"] = [bar.v for bar in data]

        return df

e = session()

data = e.get_history("AAPL", "1D", "2023-01-01")

print(data)