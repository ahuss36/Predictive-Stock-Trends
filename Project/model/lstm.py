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
scaled_data = pd.DataFrame(scaled_data, index = raw_data['time']) #making scaled Data into a 2D array by adding timestamps



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


#Reshaping Training Data for LSTM Insertion 
#(*****PARTIAL UNDERSTANDING OF RESHAPE FUNCTION*****)
#When we reshape from a 1D to 3D array, we need to use reshape(first_column, second_column, features) where total volume of 3D Array equals total data points
lstm_ready_train_data = np.reshape(train_data, (train_data.shape[0], train_data.shape[1], 1))



#Building LSTM Model
model = Sequential()
model.add(LSTM(units = 100, return_sequences=True, ))


#TO DO POST  10/11/2023
#WE NEED TO ELIMINATE LOOK AHEAD BIAS T
#RESEARCH HOW TO DO ROLLING WINDOWS OF TEST AND TRAINING DATA
#DECIDE WHAT TYPE OF LSTM MODEL 