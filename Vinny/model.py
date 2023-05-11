from PIL import Image
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
# from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential
import warnings
warnings.filterwarnings("ignore")

# sports_keywords = ["sports", "football", "soccer", "basketball"]
# non_sports_keywords = ["music", "food", "travel"]
good_keywords = ["dog", "cute dog", "puppy", "small dog", "pet dog", "big dog"]
bad_keywords = ["house", "sports", "travel", "art", "money", "tree", "food", "computer", "code"]


df = pd.DataFrame(columns=['file_path', 'label'])

def addToDf(keyword, label):
    global df
    for image_file in os.listdir("valuationEstimator/images/" + keyword):
        df = df.append({'file_path': os.path.abspath(f"valuationEstimator/images/{keyword}/{image_file}"), 'label': label}, ignore_index=True)

# Download sports-related images
for word in good_keywords:
    addToDf(word, 1)

# Download non-sports-related images
for word in bad_keywords:
    addToDf(word, 0)

df.to_csv('image_data.csv', index=False)

# Load the CSV file
df = pd.read_csv('image_data.csv')

# Define a function to load and preprocess the images
def load_and_preprocess_image(file_path):
    # Load the image
    img = Image.open(file_path)
    # Convert the image to RGB
    img = img.convert('RGB')
    # Resize the image to 64x64
    img = img.resize((64, 64))
    # Convert the image to a numpy array and scale the pixel values
    return np.array(img) / 255.0

# Apply the function to each file path in the DataFrame
X = np.array([load_and_preprocess_image(file_path) for file_path in df['file_path']])
y = df['label'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64 ,3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

test_loss, test_acc = model.evaluate(X_test,  y_test, verbose=2)

print(f"test_loss: {test_loss}")
print(f"test_acc: {test_acc}")

# Save the entire model to a HDF5 file.
# The '.h5' extension indicates that the model should be saved to HDF5.
model.save('my_model.h5')
