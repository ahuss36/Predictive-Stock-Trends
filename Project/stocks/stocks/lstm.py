import datetime
from . import models
import pandas as pd
from pandas import DataFrame as df
import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
import alpaca

from . import lstm_functions

def trainModel(data, filename):
    return True

def loadModel(ticker):
    try:
        # load model from file
        filename = ticker.lower() + '.keras' # files should be saved as .keras
        model = keras.models.load_model(filename)
    except:
        return False
    
    return model

def saveModel(model, ticker):
    try:
        # save model to file
        filename = ticker.lower() + '.keras' # files should be saved as .keras
        model.save(filename)
        return True
    except:
        return False

def predict(ticker, daysOut=3):

    if (daysOut > 7): # no predicting more than 7 days out
        daysOut = 7

    future_predictions = []

    model = loadModel(ticker)

    if (model == False):
        return False
    
    # TODO: what is last_sequence?

    for i in range(daysOut):
        next_pred = model.predict(last_sequence.reshape(1, last_sequence.shape[0], 1))[0, 0]
        future_predictions.append(next_pred)
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[-1, 0] = next_pred  # Update the last value in the sequence with the predicted value

    """
    Technically looping through daysOut twice is wrong, but the code is way cleaner,
    and at max we are looping 7 times, so it shouldn't be a big deal
    """

    for i in range(daysOut):
        dbModel = models.Stock()

        dbModel.ticker = ticker
        dbModel.close = future_predictions[i]
        dbModel.date = datetime.datetime.now().date() + datetime.timedelta(days=i)
        dbModel.prediction = True # This HAS to be true here

        dbModel.save()
    
def train(ticker, data):

    if (type(data) != pd.DataFrame):
        return False
    
    close_prices = data['close']

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

    #Save model
    return saveModel(model, ticker)