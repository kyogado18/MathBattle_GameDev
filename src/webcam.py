import cv2
import numpy as np

class WebcamCapture:
    def __init__(self):
        self.cap = None
        self.active = False
        self.frame = None
        self.flipped = True  # default to mirror mode (feels natural)

    def toggle_flip(self):
        self.flipped = not self.flipped

    def start(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.active = True
            print("Webcam started.")
            return True
        else:
            print("No webcam found.")
            self.active = False
            return False

    def stop(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.active = False
        self.frame = None
        print("Webcam stopped.")

    def update(self):
        if not self.active or not self.cap:
            return
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame

    def _apply_flip(self, frame):
        if self.flipped:
            return cv2.flip(frame, 1)
        return frame

    def get_pygame_surface(self, display_width, display_height):
        if self.frame is None:
            return None
        import pygame
        frame = self._apply_flip(self.frame)
        resized = cv2.resize(frame, (display_width, display_height))
        rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(
            np.transpose(rgb_frame, (1, 0, 2))
        )
        return surface

    def capture_frame_for_recognition(self):
        if self.frame is None:
            return None
        frame = self._apply_flip(self.frame)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Crop center region (where the yellow guide box is)
        h, w = gray.shape
        margin_x = w // 4
        margin_y = h // 4
        cropped = gray[margin_y:h - margin_y, margin_x:w - margin_x]

        normalized = cropped.astype('float32') / 255.0
        normalized = normalized.reshape(1, cropped.shape[0], cropped.shape[1], 1)
        return normalized

    def is_available(self):
        return self.active