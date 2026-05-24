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

        if self._is_model_current():
            self.model.load_weights(self.model_path)
            print("Model loaded from cache.")
        else:
            print("Retraining model...")
            self.train_model()

        self.model.trainable = False

    def _is_model_current(self):
        if not os.path.exists(self.model_path):
            return False
        if not os.path.exists(self.version_path):
            return False
        with open(self.version_path, 'r') as f:
            return f.read().strip() == self.model_version

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

    # def train_model(self):
    #     os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
    #     (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    #     x_train = x_train.astype('float32') / 255.0
    #     x_test = x_test.astype('float32') / 255.0
    #     x_train = np.expand_dims(x_train, axis=-1)
    #     x_test = np.expand_dims(x_test, axis=-1)

    #     datagen = keras.preprocessing.image.ImageDataGenerator(
    #         rotation_range=10,
    #         zoom_range=0.1,
    #         width_shift_range=0.1,
    #         height_shift_range=0.1,
    #     )
    #     datagen.fit(x_train)

    #     self.model.fit(
    #         datagen.flow(x_train, y_train, batch_size=64),
    #         epochs=15,
    #         validation_data=(x_test, y_test),
    #         verbose=1
    #     )
    #     self.model.save_weights(self.model_path)
    #     with open(self.version_path, 'w') as f:
    #         f.write(self.model_version)
    def train_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        x_train = np.expand_dims(x_train, axis=-1)
        x_test = np.expand_dims(x_test, axis=-1)

        # Modern augmentation using tf.data — no scipy needed
        train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
        train_dataset = train_dataset.shuffle(10000).batch(64)

        # Augmentation layers applied during training
        augmentation = keras.Sequential([
            keras.layers.RandomRotation(0.1),
            keras.layers.RandomZoom(0.1),
            keras.layers.RandomTranslation(0.1, 0.1),
        ])

        def augment(images, labels):
            images = augmentation(images, training=True)
            return images, labels

        train_dataset = train_dataset.map(
            augment,
            num_parallel_calls=tf.data.AUTOTUNE
        ).prefetch(tf.data.AUTOTUNE)

        test_dataset = tf.data.Dataset.from_tensor_slices(
            (x_test, y_test)
        ).batch(64)

        print("Training with augmentation (no scipy)...")
        self.model.fit(
            train_dataset,
            epochs=15,
            validation_data=test_dataset,
            verbose=1
        )
        self.model.save_weights(self.model_path)
        with open(self.version_path, 'w') as f:
            f.write(self.model_version)

    def preprocess_image(self, image_array):
        """
        Accepts any size image array (canvas or webcam).
        Returns a clean 28x28 MNIST-format image.
        """
        image = image_array[0, :, :, 0]
        image = (image * 255).astype('uint8')

        # --- Step 1: Invert so digit is WHITE on BLACK ---
        image = cv2.bitwise_not(image)

        # --- Step 2: Denoise ---
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # --- Step 3: Adaptive threshold ---
        # Much more robust than fixed threshold —
        # works in different lighting (webcam) and stroke weights (canvas)
        binary = cv2.adaptiveThreshold(
            image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=-5
        )

        # --- Step 4: Find digit bounding box ---
        coords = cv2.findNonZero(binary)
        if coords is None or len(coords) < 10:
            # Nothing meaningful drawn — return blank
            print("Warning: no digit found in image.")
            return np.zeros((1, 28, 28, 1), dtype='float32')

        x, y, w, h = cv2.boundingRect(coords)

        # --- Step 5: Validate bounding box isn't just noise ---
        total_pixels = binary.shape[0] * binary.shape[1]
        digit_pixels = w * h
        if digit_pixels < total_pixels * 0.001:
            # Bounding box too small — likely noise
            print("Warning: digit too small, likely noise.")
            return np.zeros((1, 28, 28, 1), dtype='float32')

        # --- Step 6: Crop with padding ---
        pad = int(max(w, h) * 0.3)  # proportional padding
        x = max(0, x - pad)
        y = max(0, y - pad)
        x2 = min(binary.shape[1], x + w + 2 * pad)
        y2 = min(binary.shape[0], y + h + 2 * pad)
        cropped = binary[y:y2, x:x2]

        # --- Step 7: Make square ---
        ch, cw = cropped.shape
        if ch > cw:
            diff = ch - cw
            cropped = cv2.copyMakeBorder(
                cropped, 0, 0,
                diff // 2, diff - diff // 2,
                cv2.BORDER_CONSTANT, value=0)
        elif cw > ch:
            diff = cw - ch
            cropped = cv2.copyMakeBorder(
                cropped,
                diff // 2, diff - diff // 2,
                0, 0,
                cv2.BORDER_CONSTANT, value=0)

        # --- Step 8: Resize to 20x20 and center in 28x28 ---
        resized = cv2.resize(cropped, (20, 20), interpolation=cv2.INTER_AREA)
        final = np.zeros((28, 28), dtype='uint8')
        final[4:24, 4:24] = resized

        # --- Step 9: Light blur to match MNIST style ---
        final = cv2.GaussianBlur(final, (3, 3), 0)

        # Debug — see exactly what the model receives
        from PIL import Image as PILImage
        PILImage.fromarray(final).save("debug_input.png")

        return (final.astype('float32') / 255.0).reshape(1, 28, 28, 1)

    def predict(self, image_array):
        try:
            x = self.preprocess_image(image_array)

            # If preprocessing returned blank, reject immediately
            if x.max() < 0.1:
                print("Prediction rejected: blank image.")
                return None, 0.0

            predictions = self.model.predict(x, verbose=0)
            digit = int(np.argmax(predictions[0]))
            confidence = float(np.max(predictions[0]))

            print(f"Predicted: {digit} | Confidence: {confidence:.2f}")
            print(f"All scores: {[f'{p:.2f}' for p in predictions[0]]}")

            if confidence < 0.55:
                print("Confidence too low — rejecting.")
                return None, confidence

            return digit, confidence
        except Exception as e:
            print(f"Error in predict: {e}")
            import traceback
            traceback.print_exc()
            return 0, 0.0