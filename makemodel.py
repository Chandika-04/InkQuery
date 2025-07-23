import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Step 1: Load and Preprocess the Data
# Define categories and data directory
categories = ['apple', 'dog', 'cat']  # Replace with desired categories
data_dir = 'drawing_data'  # Update with path to your .ndjson files

# Convert Quick, Draw! strokes to a 28x28 image array
'''def draw_to_image(drawing, size=28):
    image = np.zeros((size, size))
    for stroke in drawing:
        for i in range(len(stroke[0]) - 1):
            x1, y1 = stroke[0][i], stroke[1][i]
            x2, y2 = stroke[0][i + 1], stroke[1][i + 1]
            x1, x2 = int(x1 * size / 255), int(x2 * size / 255)
            y1, y2 = int(y1 * size / 255), int(y2 * size / 255)
            image = cv2.line(image, (x1, y1), (x2, y2), 1, 1)
    return image
'''
def draw_to_image(drawing, size=28):
    image = np.zeros((size, size))
    for stroke in drawing:
        for i in range(len(stroke[0]) - 1):
            x1, y1 = stroke[0][i], stroke[1][i]
            x2, y2 = stroke[0][i + 1], stroke[1][i + 1]
            
            # Scale down from 255x255 to size x size (e.g., 28x28)
            x1, x2 = int(x1 * size / 255), int(x2 * size / 255)
            y1, y2 = int(y1 * size / 255), int(y2 * size / 255)
            
            # Use Bresenham's line algorithm to draw lines between points
            for t in np.linspace(0, 1, max(abs(x2 - x1), abs(y2 - y1)) + 1):
                x = int(x1 + t * (x2 - x1))
                y = int(y1 + t * (y2 - y1))
                if 0 <= x < size and 0 <= y < size:
                    image[y, x] = 1  # Set pixel to white (1) for the line

    return image

# Load and preprocess data from .ndjson files
def load_data(categories, data_dir, sample_size=10000):
    images = []
    labels = []
    for idx, category in enumerate(categories):
        file_path = os.path.join(data_dir, f'full_simplified_{category}.ndjson')
        with open(file_path, 'r') as f:
            drawings = [json.loads(line) for line in f][:sample_size]
            images.extend([draw_to_image(drawing['drawing']).reshape(28, 28, 1) for drawing in drawings])
            labels.extend([idx] * sample_size)
    
    images = np.array(images).astype('float32') / 255.0
    labels = to_categorical(np.array(labels), num_classes=len(categories))
    return images, labels

# Load and preprocess the data
images, labels = load_data(categories, data_dir)
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.4, random_state=42)

# Step 2: Define the CNN Model
def create_cnn_model(input_shape, num_classes):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    return model

# Initialize and compile the model
input_shape = (28, 28, 1)
num_classes = len(categories)
model = create_cnn_model(input_shape, num_classes)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 3: Train the Model
batch_size = 64
epochs = 15

history = model.fit(
    X_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_val, y_val),
    verbose=1
)

# Step 4: Evaluate the Model
val_loss, val_accuracy = model.evaluate(X_val, y_val)
print(f'Validation accuracy: {val_accuracy:.2f}')

# Step 5: Save the Model
model.save('quickdraw_simplified_cnn_model.h5')
print("Model saved as 'quickdraw_simplified_cnn_model.h5'.")

# Step 6: Make Predictions on New Drawings
# Predict and display a drawing from the validation set
new_drawing = X_val[1].reshape(1, 28, 28, 1)  # Use a validation sample as example
print(f'New_drawing is: {new_drawing}')
prediction = model.predict(new_drawing)
predicted_label = categories[np.argmax(prediction)]

plt.imshow(new_drawing.reshape(28, 28), cmap='gray')
plt.title(f'Predicted: {predicted_label}')
plt.savefig('predicted_drawing.png')
print("Prediction saved as 'predicted_drawing.png'.")

