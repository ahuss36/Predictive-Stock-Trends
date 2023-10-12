import pandas as pd
import numpy as np

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

def smooth(data, period): # Simple moving average

    if (data is pd.DataFrame):
        data = data['close']

    output = []

    for i in range(len(data)):
        if (i < period):
            output.append(np.mean(data[0:i+period]))
        elif (i + period > len(data)):
            output.append(np.mean(data[i:len(data)]))
        else:
            output.append(np.mean(data[i - period:i + period]))

    return output


data = [7, 3, 7, 3, 9, 3, 6, 9, 1]

print(smooth(data, 3))