import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

class DigitRecognizer:
    def __init__(self):
        self.model_path = 'assets/mnist_model.weights.h5'
        self.model = self.build_model()
        if os.path.exists(self.model_path):
            self.model.load_weights(self.model_path)
        else:
            print("Training TensorFlow MNIST model...")
            self.train_model()
        self.model.trainable = False
    
    def build_model(self):
        model = keras.Sequential([
            keras.layers.Input(shape=(28, 28, 1)),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def train_model(self):
        (x_train, y_train), _ = keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_train = np.expand_dims(x_train, axis=-1)
        self.model.fit(x_train, y_train, epochs=5, batch_size=64)
        self.model.save_weights(self.model_path)
    
    def preprocess_image(self, image_array):
        image = image_array[0, :, :, 0]
        image = (image * 255).astype('uint8')
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thresh = cv2.bitwise_not(thresh)
        resized = cv2.resize(thresh, (28, 28))
        normalized = resized.astype('float32') / 255.0
        normalized = normalized.reshape(1, 28, 28, 1)
        return normalized
    
    def predict(self, image_array):
        try:
            x = self.preprocess_image(image_array)
            predictions = self.model.predict(x, verbose=0)
            digit = int(np.argmax(predictions[0]))
            confidence = float(np.max(predictions[0]))
            return digit, confidence
        except Exception as e:
            print(f"Error in predict: {e}")
            import traceback
            traceback.print_exc()
            return 0, 0.0