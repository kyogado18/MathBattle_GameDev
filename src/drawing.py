import pygame
import numpy as np
from PIL import Image

class DrawingCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.drawing = False
        self.last_pos = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.drawing = True
                self.last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
                self.last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                # Adjust mouse position relative to canvas position
                mouse_x, mouse_y = event.pos
                canvas_x = mouse_x - 200  # Assuming canvas is drawn at 200, 150
                canvas_y = mouse_y - 150
                if 0 <= canvas_x < self.width and 0 <= canvas_y < self.height:
                    if self.last_pos:
                        last_x = self.last_pos[0] - 200
                        last_y = self.last_pos[1] - 150
                        pygame.draw.line(self.surface, (0, 0, 0), (last_x, last_y), (canvas_x, canvas_y), 5)
                    self.last_pos = event.pos
    
    def update(self):
        pass
    
    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
    
    def clear(self):
        self.surface.fill((255, 255, 255))
    
    def get_image(self):
        # Convert pygame surface to PIL Image
        string_image = pygame.image.tostring(self.surface, 'RGB')
        pil_image = Image.frombytes('RGB', (self.width, self.height), string_image)
        # Convert to grayscale and resize to 28x28 for MNIST
        pil_image = pil_image.convert('L')
        pil_image = pil_image.resize((28, 28), Image.Resampling.LANCZOS)
        # Invert colors (white background to black)
        pil_image = Image.eval(pil_image, lambda x: 255 - x)
        return pil_image
    
    def get_array(self):
        img = self.get_image()
        array = np.array(img)
        array = array.astype('float32') / 255.0
        array = array.reshape(1, 28, 28, 1)
        return array