# Predictive Stock Trends

##  Overview
Predictive Stock Trends is a machine learning project that applies **Long Short-Term Memory (LSTM)** neural networks to forecast stock price movements. The goal of this project is to leverage historical financial data to detect predictive signals, generate short-term forecasts, and provide an intuitive front-end for users to interact with the model’s outputs. 

##  Features
- **LSTM-based Forecasting**: Uses deep recurrent neural networks (Keras/TensorFlow) for time-series prediction.  
- **Data Preprocessing**: Cleans and scales stock data using Python, NumPy, and pandas.  
- **Evaluation Metrics**: Performance validated with RMSE and accuracy measures.  
- **Visualization**: Matplotlib plots comparing predicted vs. actual stock prices.  
- **Future Forecasting**: Ability to generate projections for upcoming trading days.  
- **Integration-Ready**: Includes an Alpaca Markets API wrapper for live data retrieval and simulated trading.  

- ##  Tech Stack 
- **Languages**: Python (NumPy, pandas, matplotlib, scikit-learn)  
- **Machine Learning**: TensorFlow / Keras (LSTM models)  
- **APIs**: Alpaca Markets (stock data & paper trading)  
- **Web Development**: Flask + HTML/CSS (initial UI prototype)

- ## 📖 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/predictive-stock-trends.git
cd predictive-stock-trends

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the LSTM model
python final_lstm.py
```

##  Optional: Using Alpaca API for Live Data
To integrate with **Alpaca Markets** for real-time stock data and paper trading:  

1. Replace the placeholder API keys in `alpaca.py` with your own.  
2. Run the following in Python:  

```python
from alpaca import session
s = session()
print(s.get_history('AAPL', '1D', '2020-01-01'))

```

##  Team & Contributions

Team Members: Owen Siemons, Shyamala Vasireddy, 
Aditya Ramesh, Drew Oberweis, Ali Hussain

Project Mentor: Chen Si

##  Future Work
- Enhance hyperparameter tuning for better accuracy.  
- Expand beyond single stock predictions into portfolio-level analysis.  
- Deploy a production-ready full-stack application with live data streams.  
