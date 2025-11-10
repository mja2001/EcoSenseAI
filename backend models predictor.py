import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = "co2_model.h5"  # Renamed from lstm_model.h5 for clarity

def build_and_train_model():
    # Load sample data
    df = pd.read_csv("../../data/co2_historical.csv")  # Assume columns: timestamp, co2
    data = df['co2'].values.reshape(-1, 1)
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Prepare sequences (window=10 from first doc)
    X, y = [], []
    for i in range(10, len(scaled_data)):
        X.append(scaled_data[i-10:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Build LSTM
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(10, 1)),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)  # Train
    model.save(MODEL_PATH)
    return model, scaler

def predict_co2_spike(current_co2: float) -> tuple:
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        scaler = MinMaxScaler()  # In prod, save scaler too
        # Use synthetic sequence (merged from first doc)
        sample_data = np.array([[300 + i*20] for i in range(9)] + [[current_co2]])
        scaled = scaler.fit_transform(sample_data)
        X = scaled[-10:].reshape(1, 10, 1)  # Last 10 for prediction
        pred_scaled = model.predict(X, verbose=0)[0][0]
        pred = scaler.inverse_transform([[pred_scaled]])[0][0]
        return ("Spike likely", pred) if pred > 600 else ("Normal", pred)
    except FileNotFoundError:
        # Fallback if no model
        return ("Normal (train model first)", 0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        build_and_train_model()
        print("Model trained and saved!")
    else:
        print(predict_co2_spike(550))  # Test predict