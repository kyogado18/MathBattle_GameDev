import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

class DigitRecognizer:
    def __init__(self):
        self.model_path = 'assets/mnist_model.weights.h5'
        self.model_version = 'v2'
        self.version_path = 'assets/model_version.txt'
        self.model = self.build_model()
        if os.path.exists(self.model_path):
            self.model.load_weights(self.model_path)
        else:
            print("Training TensorFlow MNIST model...")
            self.train_model()
        self.model.trainable = False
    
    # def build_model(self):
    #     model = keras.Sequential([
    #         keras.layers.Input(shape=(28, 28, 1)),
    #         keras.layers.Conv2D(32, (3, 3), activation='relu'),
    #         keras.layers.MaxPooling2D((2, 2)),
    #         keras.layers.Conv2D(64, (3, 3), activation='relu'),
    #         keras.layers.MaxPooling2D((2, 2)),
    #         keras.layers.Flatten(),
    #         keras.layers.Dense(128, activation='relu'),
    #         keras.layers.Dense(10, activation='softmax')
    #     ])
    #     model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    #     return model

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Input(shape=(28, 28, 1)),

            keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),

            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            keras.layers.BatchNormalization(),
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Dropout(0.25),

            keras.layers.Flatten(),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        (x_train, y_train), _ = keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_train = np.expand_dims(x_train, axis=-1)
        self.model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.1)
        self.model.save_weights(self.model_path)
    
    # def train_model(self):
    #     os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
    #     (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    #     x_train = x_train.astype('float32') / 255.0
    #     x_test = x_test.astype('float32') / 255.0
    #     x_train = np.expand_dims(x_train, axis=-1)
    #     x_test = np.expand_dims(x_test, axis=-1)

    #     # Augmentation — makes model robust to shifting, zooming, rotating
    #     datagen = keras.preprocessing.image.ImageDataGenerator(
    #         rotation_range=10,        # slight rotation
    #         zoom_range=0.1,           # slight zoom
    #         width_shift_range=0.1,    # shift left/right
    #         height_shift_range=0.1,   # shift up/down
    #     )
    #     datagen.fit(x_train)

    #     print("Training with augmentation...")
    #     self.model.fit(
    #         datagen.flow(x_train, y_train, batch_size=64),
    #         epochs=15,
    #         validation_data=(x_test, y_test),
    #         verbose=1
    #     )
    #     self.model.save_weights(self.model_path)


    # def preprocess_image(self, image_array):
    #     image = image_array[0, :, :, 0]
    #     image = (image * 255).astype('uint8')
    #     blurred = cv2.GaussianBlur(image, (3, 3), 0)
    #     _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #     thresh = cv2.bitwise_not(thresh)
    #     resized = cv2.resize(thresh, (28, 28))
    #     normalized = resized.astype('float32') / 255.0
    #     normalized = normalized.reshape(1, 28, 28, 1)
    #     return normalized
    
    # def preprocess_image(self, image_array):
    #     # Convert back to uint8 image
    #     image = image_array[0, :, :, 0]
    #     image = (image * 255).astype('uint8')
        
    #     # Find the bounding box of the drawn digit
    #     coords = cv2.findNonZero(image)
        
    #     if coords is None:
    #         # Nothing drawn — return blank
    #         return image_array
        
    #     x, y, w, h = cv2.boundingRect(coords)
        
    #     # Add padding around the digit
    #     padding = 20
    #     x = max(0, x - padding)
    #     y = max(0, y - padding)
    #     w = min(image.shape[1] - x, w + 2 * padding)
    #     h = min(image.shape[0] - y, h + 2 * padding)
        
    #     # Crop to the digit
    #     cropped = image[y:y+h, x:x+w]
        
    #     # Make it square by padding the shorter side
    #     if h > w:
    #         diff = h - w
    #         cropped = cv2.copyMakeBorder(
    #             cropped, 0, 0,
    #             diff // 2, diff - diff // 2,
    #             cv2.BORDER_CONSTANT, value=0
    #         )
    #     elif w > h:
    #         diff = w - h
    #         cropped = cv2.copyMakeBorder(
    #             cropped,
    #             diff // 2, diff - diff // 2,
    #             0, 0,
    #             cv2.BORDER_CONSTANT, value=0
    #         )
        
    #     # Resize to 20x20 (MNIST standard — leave room for centering)
    #     resized = cv2.resize(cropped, (20, 20), interpolation=cv2.INTER_AREA)
        
    #     # Place the 20x20 digit in the center of a 28x28 canvas
    #     final = np.zeros((28, 28), dtype='uint8')
    #     final[4:24, 4:24] = resized
        
    #     # Smooth it slightly
    #     final = cv2.GaussianBlur(final, (3, 3), 0)
        
    #     # Normalize
    #     normalized = final.astype('float32') / 255.0
    #     normalized = normalized.reshape(1, 28, 28, 1)
    #     return normalized
    
    def preprocess_image(self, image_array):
        image = image_array[0, :, :, 0]
        image = (image * 255).astype('uint8')

        # Canvas is white background, black drawing
        # Invert so digit is WHITE on BLACK (MNIST format)
        image = cv2.bitwise_not(image)

        # Find bounding box of the drawn digit
        coords = cv2.findNonZero(image)
        if coords is None:
            return np.zeros((1, 28, 28, 1), dtype='float32')

        x, y, w, h = cv2.boundingRect(coords)

        # Add padding
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)

        # Crop to digit
        cropped = image[y:y+h, x:x+w]

        # Make square
        if h > w:
            diff = h - w
            cropped = cv2.copyMakeBorder(
                cropped, 0, 0,
                diff // 2, diff - diff // 2,
                cv2.BORDER_CONSTANT, value=0)
        elif w > h:
            diff = w - h
            cropped = cv2.copyMakeBorder(
                cropped,
                diff // 2, diff - diff // 2,
                0, 0,
                cv2.BORDER_CONSTANT, value=0)

        # Resize to 20x20 then pad to 28x28
        resized = cv2.resize(cropped, (20, 20), interpolation=cv2.INTER_AREA)
        final = np.zeros((28, 28), dtype='uint8')
        final[4:24, 4:24] = resized

        # Save debug image AFTER all processing so you see exactly what model gets
        from PIL import Image as PILImage
        PILImage.fromarray(final).save("debug_input.png")

        # Normalize
        normalized = final.astype('float32') / 255.0
        return normalized.reshape(1, 28, 28, 1)
    
    # def predict(self, image_array):
    #     try:
    #         x = self.preprocess_image(image_array)
    #         predictions = self.model.predict(x, verbose=0)
    #         digit = int(np.argmax(predictions[0]))
    #         confidence = float(np.max(predictions[0]))
    #         return digit, confidence
    #     except Exception as e:
    #         print(f"Error in predict: {e}")
    #         import traceback
    #         traceback.print_exc()
    #         return 0, 0.0

    def predict(self, image_array):
        try:
            x = self.preprocess_image(image_array)
            predictions = self.model.predict(x, verbose=0)
            digit = int(np.argmax(predictions[0]))
            confidence = float(np.max(predictions[0]))

            # Reject if not confident enough
            if confidence < 0.6:
                return None, confidence  # Signal to ask player to redraw

            return digit, confidence
        except Exception as e:
            print(f"Error in predict: {e}")
            return 0, 0.0