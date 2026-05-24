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
        self.eraser_mode = False  # False = draw, True = erase
        self.brush_size = 4
        self.eraser_size = 20

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode

    def is_inside(self, pos, offset_x, offset_y):
        x, y = pos
        return (offset_x <= x < offset_x + self.width and
                offset_y <= y < offset_y + self.height)

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
                    curr_x = event.pos[0] - offset_x
                    curr_y = event.pos[1] - offset_y

                    if self.eraser_mode:
                        # Erase by drawing white
                        pygame.draw.line(
                            self.surface, (255, 255, 255),
                            (last_x, last_y), (curr_x, curr_y),
                            self.eraser_size
                        )
                        # Also draw a white circle at cursor for smooth erasing
                        pygame.draw.circle(
                            self.surface, (255, 255, 255),
                            (curr_x, curr_y), self.eraser_size // 2
                        )
                    else:
                        pygame.draw.line(
                            self.surface, (0, 0, 0),
                            (last_x, last_y), (curr_x, curr_y),
                            self.brush_size
                        )
                        # Circle at endpoints for smoother strokes
                        pygame.draw.circle(
                            self.surface, (0, 0, 0),
                            (curr_x, curr_y), self.brush_size // 2
                        )
                self.last_pos = event.pos
            else:
                self.last_pos = None

    def update(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x, y))
        # Draw eraser cursor indicator
        if self.eraser_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.is_inside((mouse_x, mouse_y), x, y):
                pygame.draw.circle(
                    screen, (200, 200, 200),
                    (mouse_x, mouse_y), self.eraser_size // 2, 2
                )

    def clear(self):
        self.surface.fill((255, 255, 255))
        self.eraser_mode = False  # reset to draw mode on clear

    def get_array(self):
        """
        Return the FULL canvas as a float32 array.
        Do NOT resize here — let the recognizer handle it.
        White background, black drawing (recognizer will invert).
        """
        string_image = pygame.image.tostring(self.surface, 'RGB')
        pil_image = Image.frombytes('RGB', (self.width, self.height), string_image)
        pil_image = pil_image.convert('L')  # grayscale only, no resize, no invert
        array = np.array(pil_image)
        array = array.astype('float32') / 255.0
        array = array.reshape(1, self.height, self.width, 1)
        return array