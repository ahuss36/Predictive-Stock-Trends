import pandas as pd
import numpy as np
import alpaca

def volatility(data):

    if (data is pd.DataFrame):
        data = data['close']

    # Calculate daily returns
    daily_returns = data.pct_change()

    # Calculate standard deviation of daily returns
    std_dev = np.std(daily_returns)

    # Annualize standard deviation
    annualized_std_dev = std_dev * np.sqrt(252)

    return annualized_std_dev