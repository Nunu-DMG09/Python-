
# Programador: David Mesta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM

df = pd.read_csv("market_data.csv")

print(df.info())  
print(df.describe()) 
print(df.isnull().sum())  

plt.figure(figsize=(10, 5))
sns.histplot(df['Close'], bins=30, kde=True)
plt.title("Distribución de precios de cierre")
plt.show()

df.fillna(df.mean(), inplace=True)  
df['Date'] = pd.to_datetime(df['Date'])  
df = df.sort_values('Date')  

df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
X = df[['Open', 'High', 'Low', 'Volume']]
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_test)

accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Precisión del modelo Random Forest: {accuracy_rf:.2f}")

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model_lstm = Sequential([
    LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1), return_sequences=True),
    LSTM(50, activation='relu'),
    Dense(1, activation='sigmoid')
])

model_lstm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
X_train_reshaped = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test_reshaped = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
model_lstm.fit(X_train_reshaped, y_train, epochs=10, batch_size=16, validation_data=(X_test_reshaped, y_test))

loss, accuracy_lstm = model_lstm.evaluate(X_test_reshaped, y_test)
print(f"Precisión del modelo LSTM: {accuracy_lstm:.2f}")

plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label="Real")
plt.plot(model_lstm.predict(X_test_reshaped), label="Predicción", linestyle="dashed")
plt.legend()
plt.title("Comparación de tendencias del mercado")
plt.show()


