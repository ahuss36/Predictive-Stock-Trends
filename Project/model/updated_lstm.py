import pandas as pd
from pandas import DataFrame as df
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import alpaca
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split



#Grabbing Initial Data
raw_data = pd.read_csv('drew_sample_data.csv')
#print(raw_data.head())


"""
#Plotting initial data
plt.figure(figsize=(10,20)) #size of window
plt.title('Plotting Original Data')
plt.xlabel('Dates')
plt.ylabel('Dollars')
plt.plot(raw_data['time'], raw_data['close']) #plotting data by columns
plt.show()
"""


#Preprocessing the Data
raw_close_data = raw_data['close'].values

scaler = MinMaxScaler(feature_range=(0,1)) #setting up the scaler to work between 0 and 1 for each data point
scaled_data = raw_close_data.reshape(-1,1) #.reshape(-1,1) if feature and .reshape(1, -1) Making this into a 2D array
scaled_data = scaler.fit_transform(scaled_data) #transforming the data into 0 to 1 for standarization 




#Prepare the training set
train_data, test_data = train_test_split(scaled_data, test_size = 0.2, random_state=42) #spits data into to and randomizes order for better training


"""
#Checking to see the data is split 
plt.figure(figsize=(20, 10)) #size of window
plt.title('Plotting Original Data')
plt.xlabel('Dates')
plt.ylabel('Dollars')
plt.plot(train_data, color = 'blue') #plotting the train_data blue
plt.plot(test_data, color = 'red') #plotting the test_data red
plt.show()
"""


#Prepare the test set

