gmport os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from shapely.geometry import LineString

def simplify_drawing(drawing, epsilon=2.0):
    """
    Applies the simplification process to a Quick, Draw! drawing.
    
    Parameters:
        drawing (list): A list of strokes, where each stroke is a list of [x_points, y_points].
        epsilon (float): The Ramer–Douglas–Peucker simplification threshold.

    Returns:
        list: A simplified and normalized drawing.
    """
    simplified_drawing = []

    # Step 1: Align to Top-Left (Make min x and min y = 0)
    all_x = [x for stroke in drawing for x in stroke[0]]
    all_y = [y for stroke in drawing for y in stroke[1]]
    
    min_x, min_y = min(all_x), min(all_y)

    for stroke in drawing:
        x_points = np.array(stroke[0]) - min_x  # Align x to 0
        y_points = np.array(stroke[1]) - min_y  # Align y to 0
        simplified_drawing.append([x_points.tolist(), y_points.tolist()])

    # Step 2: Uniform Scaling to 255x255
    all_x = [x for stroke in simplified_drawing for x in stroke[0]]
    all_y = [y for stroke in simplified_drawing for y in stroke[1]]

    max_x, max_y = max(all_x), max(all_y)
    scale = 255.0 / max(max_x, max_y) if max(max_x, max_y) > 0 else 1  # Avoid division by zero

    scaled_drawing = []
    for stroke in simplified_drawing:
        x_scaled = (np.array(stroke[0]) * scale).astype(int)
        y_scaled = (np.array(stroke[1]) * scale).astype(int)
        scaled_drawing.append([x_scaled.tolist(), y_scaled.tolist()])

    # Step 3: Resample Strokes with 1-Pixel Spacing
    def resample_stroke(x_points, y_points):
        resampled_x, resampled_y = [x_points[0]], [y_points[0]]
        for i in range(1, len(x_points)):
            x1, y1 = resampled_x[-1], resampled_y[-1]
            x2, y2 = x_points[i], y_points[i]
            distance = euclidean((x1, y1), (x2, y2))

            if distance >= 1:  # Add intermediate points if necessary
                num_steps = int(distance)  # Ensure 1-pixel spacing
                for t in np.linspace(0, 1, num_steps, endpoint=False):
                    new_x = int(x1 + t * (x2 - x1))
                    new_y = int(y1 + t * (y2 - y1))
                    resampled_x.append(new_x)
                    resampled_y.append(new_y)

            resampled_x.append(x2)
            resampled_y.append(y2)

        return resampled_x, resampled_y

    resampled_drawing = []
    for stroke in scaled_drawing:
        x_resampled, y_resampled = resample_stroke(stroke[0], stroke[1])
        resampled_drawing.append([x_resampled, y_resampled])

    # Step 4: Simplify Strokes using Ramer–Douglas–Peucker Algorithm
    def rdp_simplify(x_points, y_points, epsilon):
        """
        Applies the Ramer–Douglas–Peucker algorithm for stroke simplification.
        """
        if len(x_points) < 3:  # Not enough points to simplify
            return x_points, y_points
        
        line = LineString(zip(x_points, y_points))
        simplified_line = line.simplify(epsilon, preserve_topology=False)

        x_simplified, y_simplified = zip(*simplified_line.coords)
        return list(map(int, x_simplified)), list(map(int, y_simplified))

    final_drawing = []
    for stroke in resampled_drawing:
        x_simplified, y_simplified = rdp_simplify(stroke[0], stroke[1], epsilon)
        final_drawing.append([x_simplified, y_simplified])

    return final_drawing

data_dir = 'drawing_data'
categories = ['apple', 'dog', 'cat']

#get model first
model = tf.keras.models.load_model('quickdraw_simplified_cnn_model.h5')

#get drawing data needs draw to image and load data
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

def load_data(categories, data_dir, sample_size=5000):
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

images, labels = load_data(categories, data_dir)
print(f'length of images is : {len(images)} and length of labels is {len(labels)}')

'''my_drawing = draw_to_image(simplify_drawing()).reshape(28,28,1)

drawing_to_predict = my_drawing.reshape(1, 28, 28, 1)
prediction = model.predict(drawing_to_predict)
predicted_label = categories[np.argmax(prediction)]

plt.imshow(drawing_to_predict.reshape(28, 28), cmap='gray')
plt.title(f'Predicted: {predicted_label}')
plt.savefig('my_predicted_drawing.png')
print("Prediction saved as 'my_predicted_drawing.png'.")'''

for i in range(15):
    new_drawing = images[i*1001].reshape(1, 28, 28, 1)  # Use a validation sample as example
    prediction = model.predict(new_drawing)
    print(f'prediction {i*1001} is {prediction}')
    predicted_label = categories[np.argmax(prediction)]

    plt.imshow(new_drawing.reshape(28, 28), cmap='gray')
    plt.title(f'Predicted: {predicted_label}')
    filename = f'predicted_drawing{i*1001}.png'
    plt.savefig(filename)
    #print(f'image {i} is {images[i]}')
    print(f'label {i*1001} is {labels[i*1001]}')

