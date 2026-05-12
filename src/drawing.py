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
    
    def is_inside(self, pos, offset_x, offset_y):
        x, y = pos
        return offset_x <= x < offset_x + self.width and offset_y <= y < offset_y + self.height
    
    def handle_event(self, event, offset_x, offset_y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_inside(event.pos, offset_x, offset_y):
                self.drawing = True
                self.last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
                self.last_pos = None
        elif event.type == pygame.MOUSEMOTION and self.drawing:
            if self.is_inside(event.pos, offset_x, offset_y):
                if self.last_pos and self.is_inside(self.last_pos, offset_x, offset_y):
                    last_x = self.last_pos[0] - offset_x
                    last_y = self.last_pos[1] - offset_y
                    current_x = event.pos[0] - offset_x
                    current_y = event.pos[1] - offset_y
                    pygame.draw.line(self.surface, (0, 0, 0), (last_x, last_y), (current_x, current_y), 5)
                self.last_pos = event.pos
            else:
                self.last_pos = None
    
    def update(self):
        pass
    
    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
    
    def clear(self):
        self.surface.fill((255, 255, 255))
    
    def get_image(self):
        string_image = pygame.image.tostring(self.surface, 'RGB')
        pil_image = Image.frombytes('RGB', (self.width, self.height), string_image)
        pil_image = pil_image.convert('L')
        pil_image = pil_image.resize((28, 28), Image.Resampling.LANCZOS)
        pil_image = Image.eval(pil_image, lambda x: 255 - x)
        return pil_image
    
    def get_array(self):
        img = self.get_image()
        array = np.array(img)
        array = array.astype('float32') / 255.0
        array = array.reshape(1, 28, 28, 1)
        return array