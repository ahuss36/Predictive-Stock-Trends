from . import models
import pandas as pd
import tensorflow as tf
import keras

def trainModel(data, filename):
    return True

def loadModel(filename):
    try:
        # load model from file
        model = keras.models.load_model(filename)

def predict(data, daysOut=3):

    if (daysOut > 7):
        daysOut = 7

    def addPredictionValues(values): # save a dataframe of values to the database as predictions

        """
        Takes a dataframe of this structure:
        ticker | close | date
        """

        if (type(values) != pd.DataFrame): # This needs a dataframe for the data
            return False
        
        for i in range(0, daysOut):
            dbModel = models.Stock()

            dbModel.ticker = values.iloc[i].ticker # I don't know what iloc is
            dbModel.close = values.iloc[i].close
            dbModel.date = values.iloc[i].date
            dbModel.prediction = True # This HAS to be true here

            dbModel.save()

        return True