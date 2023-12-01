import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt


def create_sequences(data, seq_length):
    sequences = []
    targets = []
    for i in range(len(data) - seq_length):
        seq = data[i:i + seq_length]
        target = data[i + seq_length]
        sequences.append(seq)
        targets.append(target)
    return np.array(sequences), np.array(targets)

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mse', metrics = ['accuracy'])
    return model
    
def train_model(model, X_train, y_train, epochs=50, batch_size=32):
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

def plot_results(y_test, predictions, future_predictions=None):
    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='Actual Stock Price', color='orange')
    plt.plot(predictions, label='Predicted Stock Price', color='green')

    if future_predictions is not None:
        plt.plot(range(len(y_test), len(y_test) + len(future_predictions)), future_predictions,
                 label='Future Predictions', color='blue')

    plt.title('Stock Price Prediction and Future Forecast using LSTM')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

def predict_future_prices(model, last_sequence, n_steps):
    future_predictions = []

    for i in range(n_steps):
        next_pred = model.predict(last_sequence.reshape(1, last_sequence.shape[0], 1))[0, 0]
        future_predictions.append(next_pred)
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[-1, 0] = next_pred  # Update the last value in the sequence with the predicted value

    return future_predictions