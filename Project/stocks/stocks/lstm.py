import datetime
import pandas as pd
from pandas import DataFrame as df
import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from . import models
from . import alpaca
from . import lstm_functions

def loadModel(ticker): # Load a given ticker's LSTM model, or train a new one if it doesn't exist
    try:
        # load model from file
        filename = ticker.lower() + '.keras' # files should be saved as .keras
        model = keras.models.load_model(filename)
    except (FileNotFoundError, OSError): # if the file does not exist, train a new model
        data = models.Stock.objects.filter(ticker=ticker) # pull data for stock
        model = train(ticker, data) # train new model

        return model # return newly trained model
    
    return model

def saveModel(model, ticker):
    try:
        # save model to file
        filename = ticker.lower() + '.keras' # files should be saved as .keras
        model.save(filename)
        return model
    except:
        return False

def predict(ticker, daysOut=3):

    if (daysOut > 7): # no predicting more than 7 days out
        daysOut = 7

    future_predictions = []

    model = loadModel(ticker)

    if (model == False): # if loadModel errored out, return False here and let something else handle it
        return False
    
    data = models.Stock.objects.filter(ticker=ticker) # pull raw data
    windows = lstm_functions.create_sequences(data, 60) # generate windows

    last_sequence = windows[-1] # grab last window

    for i in range(daysOut):
        next_pred = model.predict(last_sequence.reshape(1, last_sequence.shape[0], 1))[0, 0]
        future_predictions.append(next_pred)
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[-1, 0] = next_pred  # Update the last value in the sequence with the predicted value

    """
    Technically looping through daysOut twice is wrong, but the code is way cleaner,
    and at max we are looping 7 times, so it shouldn't be a big deal
    """

    for i in range(daysOut): # saving the predictions to database
        dbModel = models.Stock()

        dbModel.ticker = ticker
        dbModel.close = future_predictions[i]
        dbModel.date = datetime.datetime.now().date() + datetime.timedelta(days=i) # today's date plus 'i'
        dbModel.prediction = True # This HAS to be true here

        dbModel.save()
    
def train(ticker, data): # Train a new model from scratch

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

# TODO: ability to retrain a model based on new data