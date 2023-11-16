import pandas as pd
from pandas import DataFrame as df
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
import alpaca
import lstm_functions



#Grabbing the Initial Data
# get_history('AAPL', '1D', '2020-01-01', '2020-01-10'), end date is optional
raw_data = alpaca.session().get_history('AAPL', '1H', '2015-01-01')
close_prices = raw_data['close']


#Normalize Data
scaler = MinMaxScaler(feature_range=(0,1))
close_prices_scaled = scaler.fit_transform(close_prices.values.reshape(-1, 1))

#Set the rolling window size
window_size = 60

#Create seqeunces and targets
X, y = lstm_functions.create_sequences(close_prices_scaled, window_size)

#Split the data into training and testing sets
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


#Reshaping the Data for the LSTM input (samples, time steps, functions)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

#Building and training the LSTM Model
input_shape = (X_train.shape[1], 1)
model = lstm_functions.build_lstm_model(input_shape)
lstm_functions.train_model(model, X_train, y_train, epochs = 11, batch_size = 128)

#Making predictions on the test set
predictions = model.predict(X_test)

# Inverse transform the predictions and actual values to original scale
predictions = scaler.inverse_transform(predictions)
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# Plot the results
lstm_functions.plot_results(y_test, predictions)



# Number of days to predict into the future
n_days_future = 7

# Predict future stock prices
last_sequence = X_test[-1]
future_predictions = lstm_functions.predict_future_prices(model, last_sequence, n_days_future)

# Inverse transform the future predictions to the original scale
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Plot the results including future predictions
lstm_functions.plot_results(y_test, predictions, future_predictions)








