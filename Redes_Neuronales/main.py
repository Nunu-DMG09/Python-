# Programador: David Mesta

import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

X = np.array([
    [15000, 80000, 100],  
    [30000, 40000, 200],  
    [45000, 20000, 300],  
    [12000, 100000, 90],  
    [35000, 30000, 250]
])


y = np.array([0, 1, 1, 0, 1])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(3,)),  # Capa oculta 1
    keras.layers.Dense(4, activation='relu'),  # Capa oculta 2
    keras.layers.Dense(1, activation='sigmoid')  # Capa de salida (0 o 1)
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=50, verbose=0)

loss, accuracy = model.evaluate(X_test, y_test)
print(f"✅ Precisión del modelo: {accuracy:.2%}")

# 🚗 Hacer una predicción
nuevo_auto = np.array([[25000, 50000, 150]])  # Auto con precio 25000, 50000 km, 150 HP
prediccion = model.predict(nuevo_auto)

# Mostrar resultado
if prediccion > 0.5:
    print("💰 El auto es LUJOSO")
else:
    print("💲 El auto es ECONÓMICO")
