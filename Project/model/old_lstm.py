import pandas as pd
from pandas import DataFrame as df
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense



#Grabbing Initial Data
raw_data = pd.read_csv('drew_sample_data.csv')
#print(raw_data.head())


"""
# get_history('AAPL', '1D', '2020-01-01', '2020-01-10'), end date is optional
stock_data = alpaca.session().get_history('MSFT', '1D', '2015-01-01')
print(stock_data.head())
"""


"""
#Plotting initial data
plt.figure(figsize=(20,10)) #size of window
plt.title('Plotting Original Data')
plt.xlabel('Dates')
plt.ylabel('Dollars')
plt.plot(raw_data['time'], raw_data['close']) #plotting data by columns
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365)) #sets location of major tickers on x axis by intervals
plt.gcf().autofmt_xdate()
plt.show()
"""



#Preprocessing the Data
raw_close_data = raw_data['close'].values #1D Array
scaler = MinMaxScaler(feature_range=(0,1)) #setting up the scaler to work between 0 and 1 for each data point
scaled_data = raw_close_data.reshape(-1,1) #.reshape(-1,1) if feature and .reshape(1, -1)
scaled_data = scaler.fit_transform(scaled_data) #transforming the data into 0 to 1 for standarization 
#scaled_data = pd.DataFrame(scaled_data, index = raw_data['time']) #making scaled Data into a 2D array by adding timestamps



#Prepare the training set
train_data, test_data = train_test_split(scaled_data, test_size = 0.2, random_state=42) #spits data into to and randomizes order for better training



"""
#Checking to see the data is split 
plt.figure(figsize=(20, 10)) #size of window
plt.title('Plotting Test/Training Split Data')
plt.plot(train_data, color = 'blue') #plotting the train_data blue
plt.plot(test_data, color = 'red') #plotting the test_data red
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1825)) #sets location of major tickers on x axis by intervals
plt.gcf().autofmt_xdate()
plt.show()
"""



#Rolling Window to avoid Look-Ahead-Bias
#Splitting the train_data into a input section (time and close price) and a target section (the close we want to predict). 


#Note on naming conventions: 
#X is capital because it represents a matrix with 2D values of time and value
# #whereas y is just a vector representing just the target values we want to predict
X_train = [] #Feature Data
y_train = [] #Label Data

for i in range(60, len(train_data)): #Create a 60-days window of historical prices feature data (x_train) and the following 60-days window as label data (y_train).
    X_train.append(train_data[i-60:i, 0]) #assigning 60 before to today for input
    y_train.append(train_data[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train) #Convert the feature data (x_train) and label data (y_train) into Numpy array for NN.
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1)) #Reshape back into a three-dimensional array to train a LSTM model.


X_test = [] #Feature Data
y_test = [] #Label Data

for i in range(60, len(test_data)):
  X_test.append(test_data[i-60:i, 0])

X_test = np.array(X_test) #Convert the feature data (X_test) and label data (y_test) into Numpy array
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1)) #Reshape again the X_test and y_test into a three-dimensional array







#Building LSTM Model
#The hyperparameters to mess with include the density of the LSTM model, the type of loss measurement, and the algorithm for optimizer
model = Sequential()
model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse', metrics = ['accuracy'])
model.summary()



#Training the model
model.fit(X_train, y_train, epochs = 6, batch_size = 128)


#Predicting the Test Data 
predicted_values = model.predict(X_test)
predicted_values = scaler.inverse_transform(predicted_values)



#Plotting Actual vs Predicted
plt.figure(figsize=(20, 10))
plt.title('Actual vs. Predicted Data')
plt.plot(raw_close_data, label="Actual Data", color='blue')
plt.plot(predicted_values, label="Predicted Data", color='red')
plt.xlabel('Dates')
plt.ylabel('Dollars')
plt.legend()
plt.show()

