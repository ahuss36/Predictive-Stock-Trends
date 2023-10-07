import pandas as pd
import numpy as np
import alpaca

def volatility(data):
    # Calculate daily returns
    daily_returns = data['close'].pct_change()

    # Calculate standard deviation of daily returns
    std_dev = np.std(daily_returns)

    # Annualize standard deviation
    annualized_std_dev = std_dev * np.sqrt(252)

    return annualized_std_dev

def moving_average(data, size):
    output = []

    for i in range(len(data) - 1):
        ending = i + size
        output.append(np.mean(data[i:ending]))

    return output