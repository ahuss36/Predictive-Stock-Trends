import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import tensorflow as tf
from tensorflow import keras
from keras import layers
 
import datetime as dt
#import alpaca



#DATA RETRIEVAL
stock_data = pd.read_csv("drew_sample_data.csv")
print(stock_data.head())

"""
# get_history('AAPL', '1D', '2020-01-01', '2020-01-10'), end date is optional
stock_data = alpaca.session().get_history('MSFT', '1D', '2015-01-01')
print(stock_data.head())
"""

#DATA PREPROCESSING
close_price = stock_data['close']
values = close_price.values

scaler = MinMaxScaler(feature_range=(0,1)) #normalize all our stock data ranging from 0 to 1
scaled_data = scaler.fit_transform(values.reshape(-1, 1)) #We also reshape our normalized data into a two-dimensional array


training_data_len = math.ceil(len(values)*0.8) #Calculate  data size for 80%. math.ceil method ensures data size is rounded up to an integer.
train_data = scaled_data[0: training_data_len, :] #Set apart the first 80% of the stock data as the training set

#feature data is input. label data is output.
x_train =[] #feature data
y_train = [] #label data

for i in range(60, len(train_data)): #Create a 60-days window of historical prices feature data (x_train) and the following 60-days window as label data (y_train).
    x_train.append(train_data[i-60:i, 0]) #assigning 60 before to today for input
    y_train.append(train_data[i, 0])


x_train, y_train = np.array(x_train), np.array(y_train) #Convert the feature data (x_train) and label data (y_train) into Numpy array for NN.
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) #Reshape back into a three-dimensional array to train a LSTM model.


#PREPARING TEST SET
test_data = scaled_data[training_data_len-60: , : ] #Extract the closing prices the last 20% of the dataset

#feature data is input. label data is output.
x_test = [] #feature data
y_test = values[training_data_len:] #label data


for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test) #Convert the feature data (x_test) and label data (y_test) into Numpy array
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)) #Reshape again the x_test and y_test into a three-dimensional array


#SETTING UP LTSM
model = keras.Sequential() #A sequential model is a linear stack of layers
model.add(layers.LSTM(200, return_sequences=True, input_shape=(x_train.shape[1], 1))) #adding a layer of 100 units and having output be another sequence of the same length 
model.add(layers.LSTM(200, return_sequences=False)) #Repeat, but we set the return_sequence to false to only return the last output in the output sequence.


model.add(layers.Dense(50)) #Add a densely connected neural network layer with 25 network units
model.add(layers.Dense(1)) #add a densely connected layer that specifies the output of 1 network unit
model.summary() #Show the summary of our LSTM network architecture


#TRAINING THE LSTM MODEL
model.compile(optimizer='adam', loss='mean_squared_error') #Adopt “adam” optimizer and set the mean square error as loss function
model.fit(x_train, y_train, batch_size= 256, epochs=6) #Train the model by fitting it with the training set. epoch = 3x column number 
#(INCREASING THE BATCH SIZE DECREASES TIME AT THE COST OF ACCURACY)

#EVALUATE THE MODEL
predictions = model.predict(x_test) #Apply the model to predict the stock prices based on the test set
predictions = scaler.inverse_transform(predictions) #Use the inverse_transform method to denormalize the predicted stock prices
rmse = np.sqrt(np.mean(predictions - y_test)**2) # Apply the RMSE formula to calculate the degree of discrepancy between the predicted prices and real prices
print(rmse)

#VISUALIZE MODEL
data = stock_data.filter(['close'])
train = data[:training_data_len] #Split our stock data into three plotting regions: training, validation and prediction.
validation = data[training_data_len:]
validation['Predictions'] = predictions


plt.figure(figsize=(16,8))
plt.title('Stock Prices Prediction')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(train)
plt.plot(validation[['close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.gcf().autofmt_xdate()
plt.show()
