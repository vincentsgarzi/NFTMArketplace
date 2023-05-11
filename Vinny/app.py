import tensorflow as tf
import os
# from tensorflow import keras
from keras.models import load_model
from PIL import Image
import warnings
import numpy as np
warnings.filterwarnings("ignore")

def load_and_preprocess_image(file_path):
    # Load the image
    img = Image.open(file_path)
    # Convert the image to RGB
    img = img.convert('RGB')
    # Resize the image to 64x64
    img = img.resize((64, 64))
    # Convert the image to a numpy array and scale the pixel values
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Recreate the exact same model, including its weights and the optimizer
model = load_model('my_model.h5')

# Show the model architecture
model.summary()

for image in os.listdir("valuationEstimator/test_images"):
  data = load_and_preprocess_image(f"valuationEstimator/test_images/{image}")
  prediction = model.predict(data)
  print(f"{image} received a score of: {prediction}")
