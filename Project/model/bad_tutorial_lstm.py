#Using RMSE or MAPE to measuree how close or far off our price predictions are from the real world. 
#THIS IS A PRACTICE, HARD CODED IN SOME PLACES FOR THIS SPECIFIC AAPL HISTORY DATA SET
#FUTURE USE WILL REQUIRE CHANGES TO CALL FROM API

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as mdates
import datetime as dt


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error


#Grabbing the values from data set --> will need call API in future
stock_data = pd.read_csv("drew_sample_data.csv", index_col='time')
stock_data.head() #When printed, can be used to quickly check first 5 rows of data

#Preprocessing the Data prior to Training
target_y = stock_data['close']
X_feat = stock_data.iloc[:, 0:3]

#Feature Scaling, using StandardScaler to rescale our values between -1 and 1
sc = StandardScaler()
X_ft = sc.fit_transform(X_feat.values)
X_ft = pd.DataFrame(columns=X_feat.columns, data=X_ft, index=X_feat.index)



#There are currently 31740 data samples in the dataset
#LSTM models require windows in each training step, Example: LSTM will take 10 samples to predict #10 by weighing previous 9 inputs in one step
#Thus, cant use Sklearn train_test_split, but rather have to make own function

def lstm_split(data, n_steps):
    X, y = [], []
    for i in range(len(data)-n_steps+1):
        X.append(data[i:i + n_steps, :-1])
        y.append(data[i + n_steps-1, -1])
    
    return np.array(X), np.array(y)


#Now splitting into training and testing splits, where shuffling is not permitted (LOOK INTO FURTHER LATER)
X1, y1 = lstm_split(X_ft, n_steps=2) #n_steps is the amount of previous days of data

train_split = 0.8
split_idx = int(np.ceil(len(X1)*train_split))
date_index = stock_data.index

X_train, X_test = X1[:split_idx], X1[:split_idx]
y_train, y_test = y1[:split_idx], y1[:split_idx]
X_train_date, X_test_date = date_index[:split_idx], date_index[:split_idx]
print(X1.shape, X_train.shape, X_test.shape, y_test.shape)  #Not 100% what result means


#Building the LSTM Model
lstm = Sequential()
lstm.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2]), activation='relu', return_sequences=True))
lstm.add(LSTM(50, activation = 'relu'))

lstm.add(Dense(1))
lstm.compile(loss='mean_squared_error', optimizer='adam')
lstm.summary()

history=lstm.fit(X_train, y_train, epochs=100, batch_size=64, verbose=2, shuffle=False)



#Performance Validation on a test set
y_pred = lstm.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mape = mean_absolute_percentage_error(y_test, y_pred)
print('RSME: ', rmse)
print('MAPE: ', mape)

#Plotting the inputted data in an organized fashion
plt.figure(figsize=(15,10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) #formats major tickers on x axis by YMD time standard
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90)) #sets location of major tickers on x axis by intervals
x_dates = [dt.datetime.strptime(d, '%Y-%m-%d %H:%M:%S%z').date() for d in stock_data.index.values] #assigning x_dates to converted format for each value

plt.plot(x_dates, target_y, label='Close')
plt.plot(x_dates, y_pred, label='Predicted Close')
plt.xlabel("Time Scale")
plt.ylabel("Scaled USD")
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()




"""
#Steps to improve the model: 
1. Increase the LTSM layer until there is stangation in training (lstm.add(LSTM(X, ...)))
2. Increased time setps (n_steps)
"""



