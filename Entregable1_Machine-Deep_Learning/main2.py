import numpy as np
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Cargar datos
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# Definir modelo
model = Sequential([
    Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(2),
    Conv2D(64, 3, activation='relu'),
    MaxPooling2D(2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train_cat, epochs=5, validation_split=0.2)

# Predecir
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)

# Filtrar predicciones correctas
correct_indices = np.where(predicted_classes == y_test)[0]
selected_indices = correct_indices[:20]

# Crear grilla con predicciones encima
def plot_grid(images, predictions, indices, grid_rows=4, grid_cols=5):
    fig, axs = plt.subplots(grid_rows, grid_cols, figsize=(12, 8))
    fig.suptitle("Predicciones", fontsize=16)

    for i, idx in enumerate(indices):
        row = i // grid_cols
        col = i % grid_cols
        ax = axs[row, col]
        img = images[idx].reshape(28, 28)

        ax.imshow(img, cmap='gray')
        ax.set_title(f'{predictions[idx]}', color='lime', fontsize=16, weight='bold')
        ax.axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.show()

plot_grid(X_test, predicted_classes, selected_indices)
