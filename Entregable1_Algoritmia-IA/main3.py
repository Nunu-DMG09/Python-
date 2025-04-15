# Programador: David Mesta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score

df = pd.read_csv("dataset.csv")  # Cargar el dataset

print("Primeros registros del dataset:") # Explorar los primeros registros
print(df.head())

print("\nResumen estadístico:") # Análisis estadístico básico
print(df.describe())

matriz = df[['Edad', 'Experiencia', 'Salario']].values # Operaciones de Álgebra Lineal
vector = np.array([1, 2, 3])  # Vector de prueba
producto_punto = np.dot(matriz, vector)
print("\nProducto punto entre matriz y vector:")
print(producto_punto[:5])  # Mostramos los primeros 5 resultados

print("\nVarianza de los salarios:", np.var(df['Salario'])) # Cálculo de varianza y desviación estándar
print("Desviación estándar de los salarios:", np.std(df['Salario']))

# Gráfico de distribución de salarios
sns.histplot(df['Salario'], bins=20, kde=True)
plt.title("Distribución de Salarios")
plt.xlabel("Salario")
plt.ylabel("Frecuencia")
plt.show()

# Preparar datos para Machine Learning
X = df[['Edad', 'Experiencia', 'Educacion']]
y = df['Salario']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Predicciones
y_pred = modelo.predict(X_test)
print("\nError cuadrático medio del modelo:", mean_squared_error(y_test, y_pred))
