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
        print("Found existing model, loading...")
    except (FileNotFoundError, OSError): # if the file does not exist, train a new model
        print("Model not found, training new model")
        data = models.Stock.objects.filter(ticker=ticker) # pull data for stock
        print("Data pulled for new model training")

        # convert data to dataframe containing just list and close

        data = df(list(data.values('close')), columns=['close']) # convert to dataframe
        data['date'] = data.index # add date column
        data = data.set_index('date') # set date as index
                
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
    
    print("Loading model...")

    model = loadModel(ticker)
    if (model == False): # if loadModel errored out, return False here and let something else handle it
        print("Model failed to load")
        return False
    
    print("Model loaded")

    
    rawData = models.Stock.objects.filter(ticker=ticker) # pull raw data
    # convert data to list for sequcencing
    rawData = rawData.values('close') # convert to list of dicts
    data = []
    for i in range(len(rawData)):
        data.append(rawData[i]['close']) # convert to list of values

    scaler = MinMaxScaler(feature_range=(0,1))

    # convert data to numpy array for scaling
    data = np.array(data)
    data = scaler.fit_transform(data.reshape(-1, 1))

    print("Generating windows...")
    
    # convert data from a list of lists to a list of ints
    data = [i[0] for i in data]

    windows, targets = lstm_functions.create_sequences(data, 60) # generate windows

    print("Windows generated")
    last_sequence = windows[-1] # grab last window

    print("Predicting...")

    

    for i in range(daysOut):
        print(f"Predicting day {str(i + 1)} of {str(daysOut)}")
        next_pred = model.predict(last_sequence.reshape(1, last_sequence.shape[0], 1))[0, 0]
        future_predictions.append(next_pred)
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[-1] = next_pred  # Update the last value in the sequence with the predicted value

    print("Done predicting")
    print("Saving predictions to database")

    """
    Technically looping through daysOut twice is wrong, but the code is way cleaner,
    and at max we are looping 7 times, so it shouldn't be a big deal
    """

    # convert future_predictions into a 2d numpy array
    future_predictions = np.array(future_predictions)
    future_predictions = future_predictions.reshape(-1, 1)

    future_predictions = scaler.inverse_transform(future_predictions)

    for i in range(daysOut): # saving the predictions to database
        print(f"Saving day {i + 1} of {daysOut}, value {future_predictions[i]}")
        dbModel = models.Stock()

        dbModel.ticker = ticker
        dbModel.close = future_predictions[i]
        dbModel.date = datetime.datetime.now().date() + datetime.timedelta(days=i) # today's date plus 'i'
        dbModel.prediction = True # This HAS to be true here

        dbModel.save()

    print("Done saving predictions to database")
    
def train(ticker, data): # Train a new model from scratch

    print(f"Beginning model training for {ticker}")

    if (type(data) != pd.DataFrame):
        print("Data is not a dataframe, exiting...")
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