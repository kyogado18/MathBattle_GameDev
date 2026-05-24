# import os
# import sys
# import pygame

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.math_generator import MathGenerator
# from src.drawing import DrawingCanvas
# from src.battle import BattleSystem
# from src.ui import UI

# try:
#     from src.recognition import DigitRecognizer
# except ImportError:
#     DigitRecognizer = None

# class Game:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
#         pygame.display.set_caption("Math Battle Game")
#         self.clock = pygame.time.Clock()
#         self.running = True
        
#         self.width, self.height = self.screen.get_size()
#         self.canvas_width = 400
#         self.canvas_height = 300
#         self.canvas_x = (self.width - self.canvas_width) // 2
#         self.canvas_y = (self.height - self.canvas_height) // 2
        
#         self.math_gen = MathGenerator()
#         self.canvas = DrawingCanvas(self.canvas_width, self.canvas_height)
#         self.recognizer = DigitRecognizer() if DigitRecognizer is not None else None
#         self.battle = BattleSystem()
#         self.ui = UI()
        
#         self.current_chapter = 0  # 0: addition, 1: subtraction, etc.
#         self.chapters = ["Addition", "Subtraction", "Multiplication", "Division"]
#         self.unlocked_chapters = [True, False, False, False]  # Start with addition unlocked
        
#         self.state = "menu"  # menu, chapter_select, battle, drawing, battle_result
        
#         self.current_equation = None
#         self.player_answer = None
#         self.battle_won = False
#         self.player_confidence = 0.0
#         self.flash_timer = 0
#         self.flash_color = None
#         self.show_feedback = False
#         self.feedback_timer = 0
        
#     def run(self):
#         while self.running:
#             self.handle_events()
#             self.update()
#             self.draw()
#             self.clock.tick(60)
    
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     self.running = False
#                 elif event.key == pygame.K_SPACE:
#                     if self.state == "menu":
#                         self.state = "chapter_select"
#                     elif self.state == "chapter_select":
#                         for i, unlocked in enumerate(self.unlocked_chapters):
#                             if unlocked:
#                                 self.current_chapter = i
#                                 self.start_battle()
#                                 break
#                     elif self.state == "battle_result":
#                         self.state = "menu"
#                 elif event.key == pygame.K_RETURN and self.state == "drawing":
#                     self.submit_answer()
#             elif self.state == "drawing":
#                 self.canvas.handle_event(event, self.canvas_x, self.canvas_y)
    
#     def update(self):
#         self.width, self.height = self.screen.get_size()
#         self.canvas_x = (self.width - self.canvas_width) // 2
#         self.canvas_y = (self.height - self.canvas_height) // 2
#         if self.state == "drawing":
#             self.canvas.update()
        
#         if self.flash_timer > 0:
#             self.flash_timer -= 1
#         if self.feedback_timer > 0:
#             self.feedback_timer -= 1
#         else:
#             self.show_feedback = False
#             # After feedback fades, if waiting for next round, generate new equation
#             if self.state == "waiting_for_next_round":
#                 self.generate_new_equation()
    
#     def start_battle(self):
#         self.battle = BattleSystem()  # Reset battle
#         self.generate_new_equation()
    
#     def generate_new_equation(self):
#         self.current_equation, self.correct_answer = self.math_gen.generate_equation(self.current_chapter)
#         self.state = "drawing"
#         self.canvas.clear()
#         self.player_answer = None
    
#     def submit_answer(self):
#         # if self.recognizer is not None:
#         #     image_array = self.canvas.get_array()
#         #     result = self.recognizer.predict(image_array)
#         #     if result is None:
#         #         self.player_answer = 0
#         #         self.player_confidence = 0.0
#         #     else:
#         #         digit, confidence = result
#         #         self.player_answer = digit
#         #         self.player_confidence = confidence
#         #     correct = (self.player_answer == self.correct_answer)
#         # else:
#         #     correct = True
#         #     self.player_answer = self.correct_answer
#         #     self.player_confidence = 1.0
#         if self.recognizer is not None:
#             image_array = self.canvas.get_array()
#             result = self.recognizer.predict(image_array)
#             digit, confidence = result

#             # If confidence too low, ask to redraw
#             if digit is None:
#                 self.show_redraw_prompt = True
#                 return  # Don't submit yet

#             self.player_answer = digit
#             self.player_confidence = confidence
#             correct = (self.player_answer == self.correct_answer)
#         else:
#             correct = True
#             self.player_answer = self.correct_answer
#             self.player_confidence = 1.0
        
#         self.show_feedback = True
#         self.feedback_timer = 120  # Increased to 120 frames (~2 seconds) to see answer clearly
        
#         self.battle.player_attack_enemy(correct)
#         if correct:
#             self.flash_color = (0, 255, 0)
#         else:
#             self.flash_color = (255, 0, 0)
#         self.flash_timer = 30
        
#         if not self.battle.is_battle_over():
#             self.battle.enemy_attack_player()
#             if not self.battle.is_battle_over():
#                 # Wait for feedback to finish before generating new equation
#                 self.state = "waiting_for_next_round"
#             else:
#                 self.battle_won = False
#                 self.state = "battle_result"
#         else:
#             if self.current_chapter < 3 and not self.unlocked_chapters[self.current_chapter + 1]:
#                 self.unlocked_chapters[self.current_chapter + 1] = True
#             self.battle_won = True
#             self.state = "battle_result"
    
#     def draw(self):
#         self.screen.fill((20, 20, 40))  # Dark blue background
        
#         if self.flash_timer > 0 and self.flash_color:
#             flash_alpha = int((self.flash_timer / 30.0) * 100)
#             flash_surface = pygame.Surface(self.screen.get_size())
#             flash_surface.set_alpha(flash_alpha)
#             flash_surface.fill(self.flash_color)
#             self.screen.blit(flash_surface, (0, 0))
        
#         if self.state == "menu":
#             self.ui.draw_menu(self.screen)
#         elif self.state == "chapter_select":
#             self.ui.draw_chapter_select(self.screen, self.chapters, self.unlocked_chapters)
#         elif self.state == "battle":
#             self.ui.draw_battle(self.screen, self.battle, self.width, self.height)
#         elif self.state == "drawing" or self.state == "waiting_for_next_round":
#             self.ui.draw_equation(self.screen, self.current_equation, self.width)
#             self.ui.draw_canvas_container(self.screen, self.canvas_x, self.canvas_y, self.canvas_width, self.canvas_height)
#             self.canvas.draw(self.screen, self.canvas_x, self.canvas_y)
#             if self.show_feedback:
#                 self.ui.draw_feedback(self.screen, self.player_answer, self.correct_answer, self.player_confidence, self.width)
#             self.ui.draw_instructions(self.screen, self.width, self.height)
#             self.ui.draw_round_counter(self.screen, self.battle.round, self.battle.max_rounds, self.width)
#         elif self.state == "battle_result":
#             self.ui.draw_battle_result(self.screen, self.battle_won, self.width, self.height)
        
#         pygame.display.flip()

# if __name__ == "__main__":
#     pygame.init()
#     game = Game()
#     game.run()
#     pygame.quit()

import os
import sys
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.math_generator import MathGenerator
from src.drawing import DrawingCanvas
from src.battle import BattleSystem
from src.ui import UI
from src.webcam import WebcamCapture

try:
    from src.recognition import DigitRecognizer
except ImportError:
    DigitRecognizer = None

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Math Battle Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.width, self.height = self.screen.get_size()
        self.canvas_width = 400
        self.canvas_height = 300
        self.canvas_x = (self.width - self.canvas_width) // 2
        self.canvas_y = (self.height - self.canvas_height) // 2

        self.math_gen = MathGenerator()
        self.canvas = DrawingCanvas(self.canvas_width, self.canvas_height)
        self.recognizer = DigitRecognizer() if DigitRecognizer is not None else None
        self.battle = BattleSystem()
        self.ui = UI()
        self.webcam = WebcamCapture()

        self.current_chapter = 0
        self.chapters = ["Addition", "Subtraction", "Multiplication", "Division"]
        self.unlocked_chapters = [True, False, False, False]

        # Input mode: "canvas" or "webcam"
        self.input_mode = "canvas"

        # Accuracy tracking for recommendation system
        self.webcam_attempts = 0
        self.webcam_correct = 0
        self.LOW_ACCURACY_THRESHOLD = 0.5   # below 50% triggers warning
        self.MIN_ATTEMPTS_FOR_WARNING = 3   # need at least 3 attempts first

        self.state = "menu"

        self.current_equation = None
        self.correct_answer = None
        self.player_answer = None
        self.battle_won = False
        self.player_confidence = 0.0
        self.flash_timer = 0
        self.flash_color = None
        self.show_feedback = False
        self.feedback_timer = 0
        self.show_redraw_prompt = False
        self.show_webcam_warning = False  # low accuracy warning

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state in ("drawing", "webcam_input", "input_select"):
                        self.state = "menu"
                        self.webcam.stop()
                    else:
                        self.running = False

                elif event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.state = "chapter_select"
                    elif self.state == "battle_result":
                        self.state = "menu"
                        self.webcam.stop()
                    # Dismiss webcam warning and stay in webcam mode
                    elif self.state == "webcam_warning":
                        self.show_webcam_warning = False
                        self.state = "webcam_input"

                elif event.key == pygame.K_RETURN:
                    if self.state == "drawing":
                        self.submit_answer()
                    elif self.state == "webcam_input":
                        self.submit_webcam_answer()
                    elif self.state == "webcam_warning":
                        # Switch to canvas when pressing ENTER on warning
                        self.input_mode = "canvas"
                        self.show_webcam_warning = False
                        self.webcam.stop()
                        self.state = "drawing"
                        self.canvas.clear()

                # Input select screen — keyboard shortcuts
                elif event.key == pygame.K_1 and self.state == "input_select":
                    self._start_canvas_mode()
                elif event.key == pygame.K_2 and self.state == "input_select":
                    self._start_webcam_mode()

                # Add these inside the elif event.type == pygame.KEYDOWN block:

                # F key — toggle camera flip
                elif event.key == pygame.K_f and self.state == "webcam_input":
                    self.webcam.toggle_flip()

                # E key — toggle eraser
                elif event.key == pygame.K_e and self.state == "drawing":
                    self.canvas.toggle_eraser()

                # C key — clear canvas
                elif event.key == pygame.K_c and self.state == "drawing":
                    self.canvas.clear()

            # Mouse clicks on input select screen
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "input_select":
                    self._handle_input_select_click(event.pos)
                elif self.state == "chapter_select":
                    self._handle_chapter_click(event.pos)

            # Canvas drawing events
            if self.state == "drawing":
                self.canvas.handle_event(event, self.canvas_x, self.canvas_y)

    def _handle_chapter_click(self, pos):
        width = self.screen.get_width()
        for i, unlocked in enumerate(self.unlocked_chapters):
            if unlocked:
                y_pos = 200 + i * 100
                box_rect = pygame.Rect(width // 2 - 150, y_pos - 30, 300, 70)
                if box_rect.collidepoint(pos):
                    self.current_chapter = i
                    self.start_battle()
                    break

    def _handle_input_select_click(self, pos):
        width = self.screen.get_width()
        height = self.screen.get_height()
        canvas_rect = pygame.Rect(width // 2 - 220, height // 2 - 80, 200, 80)
        webcam_rect = pygame.Rect(width // 2 + 20, height // 2 - 80, 200, 80)
        if canvas_rect.collidepoint(pos):
            self._start_canvas_mode()
        elif webcam_rect.collidepoint(pos):
            self._start_webcam_mode()

    def _start_canvas_mode(self):
        self.input_mode = "canvas"
        self.webcam.stop()
        self.state = "drawing"
        self.canvas.clear()

    def _start_webcam_mode(self):
        self.input_mode = "webcam"
        success = self.webcam.start()
        if success:
            self.state = "webcam_input"
        else:
            # Webcam not available — fall back to canvas
            self.input_mode = "canvas"
            self.state = "drawing"
            self.canvas.clear()
            print("Webcam unavailable, falling back to canvas.")

    def update(self):
        self.width, self.height = self.screen.get_size()
        self.canvas_x = (self.width - self.canvas_width) // 2
        self.canvas_y = (self.height - self.canvas_height) // 2

        if self.state == "drawing":
            self.canvas.update()
        elif self.state == "webcam_input":
            self.webcam.update()

        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        else:
            self.show_feedback = False
            if self.state == "waiting_for_next_round":
                self.generate_new_equation()

    def start_battle(self):
        self.battle = BattleSystem()
        # Reset accuracy tracking for new battle
        self.webcam_attempts = 0
        self.webcam_correct = 0
        self.generate_new_equation()

    def generate_new_equation(self):
        self.current_equation, self.correct_answer = self.math_gen.generate_equation(self.current_chapter)
        # Show input selection before every round
        self.state = "input_select"
        self.canvas.clear()
        self.player_answer = None
        self.show_redraw_prompt = False
        self.show_webcam_warning = False

    def _check_webcam_accuracy(self):
        """Check if webcam accuracy is low and show warning if needed"""
        if self.webcam_attempts >= self.MIN_ATTEMPTS_FOR_WARNING:
            accuracy = self.webcam_correct / self.webcam_attempts
            if accuracy < self.LOW_ACCURACY_THRESHOLD:
                self.show_webcam_warning = True
                self.state = "webcam_warning"
                return True
        return False

    def submit_answer(self):
        """Handle canvas answer submission"""
        if self.recognizer is not None:
            image_array = self.canvas.get_array()
            result = self.recognizer.predict(image_array)
            digit, confidence = result

            if digit is None:
                self.show_redraw_prompt = True
                return

            self.player_answer = digit
            self.player_confidence = confidence
            correct = (self.player_answer == self.correct_answer)
        else:
            correct = True
            self.player_answer = self.correct_answer
            self.player_confidence = 1.0

        self._process_round_result(correct)

    def submit_webcam_answer(self):
        """Handle webcam answer submission"""
        if self.recognizer is not None:
            image_array = self.webcam.capture_frame_for_recognition()
            if image_array is None:
                self.show_redraw_prompt = True
                return

            result = self.recognizer.predict(image_array)
            digit, confidence = result

            if digit is None:
                self.show_redraw_prompt = True
                return

            self.player_answer = digit
            self.player_confidence = confidence
            correct = (self.player_answer == self.correct_answer)

            # Track webcam accuracy
            self.webcam_attempts += 1
            if correct:
                self.webcam_correct += 1

            # Check if we should warn about low accuracy
            if self._check_webcam_accuracy():
                return  # Warning screen will show
        else:
            correct = True
            self.player_answer = self.correct_answer
            self.player_confidence = 1.0

        self._process_round_result(correct)

    def _process_round_result(self, correct):
        """Shared logic after any answer submission"""
        self.show_feedback = True
        self.feedback_timer = 120

        self.battle.player_attack_enemy(correct)
        self.flash_color = (0, 255, 0) if correct else (255, 0, 0)
        self.flash_timer = 30

        if not self.battle.is_battle_over():
            self.battle.enemy_attack_player()
            if not self.battle.is_battle_over():
                self.state = "waiting_for_next_round"
            else:
                self.battle_won = False
                self.state = "battle_result"
                self.webcam.stop()
        else:
            if self.current_chapter < 3 and not self.unlocked_chapters[self.current_chapter + 1]:
                self.unlocked_chapters[self.current_chapter + 1] = True
            self.battle_won = True
            self.state = "battle_result"
            self.webcam.stop()

    def draw(self):
        self.screen.fill((20, 20, 40))

        if self.flash_timer > 0 and self.flash_color:
            flash_alpha = int((self.flash_timer / 30.0) * 100)
            flash_surface = pygame.Surface(self.screen.get_size())
            flash_surface.set_alpha(flash_alpha)
            flash_surface.fill(self.flash_color)
            self.screen.blit(flash_surface, (0, 0))

        if self.state == "menu":
            self.ui.draw_menu(self.screen)
        elif self.state == "chapter_select":
            self.ui.draw_chapter_select(self.screen, self.chapters, self.unlocked_chapters)
        elif self.state == "input_select":
            self.ui.draw_input_select(self.screen, self.current_equation, self.width, self.height)
        elif self.state == "drawing" or self.state == "waiting_for_next_round":
            self.ui.draw_equation(self.screen, self.current_equation, self.width)
            self.ui.draw_canvas_container(self.screen, self.canvas_x, self.canvas_y, self.canvas_width, self.canvas_height, eraser_mode=self.canvas.eraser_mode)
            self.canvas.draw(self.screen, self.canvas_x, self.canvas_y)
            if self.show_feedback:
                self.ui.draw_feedback(self.screen, self.player_answer, self.correct_answer, self.player_confidence, self.width)
            if self.show_redraw_prompt:
                self.ui.draw_redraw_prompt(self.screen, self.width, self.height)
            self.ui.draw_instructions(self.screen, self.width, self.height)
            self.ui.draw_round_counter(self.screen, self.battle.round, self.battle.max_rounds, self.width)
        elif self.state == "webcam_input" or self.state == "waiting_for_next_round":
            self._draw_webcam_screen()
        elif self.state == "webcam_warning":
            self.ui.draw_webcam_warning(
                self.screen,
                self.webcam_correct,
                self.webcam_attempts,
                self.width, self.height
            )
        elif self.state == "battle_result":
            self.ui.draw_battle_result(self.screen, self.battle_won, self.width, self.height)

        pygame.display.flip()

    def _draw_webcam_screen(self):
        """Draw the webcam feed with overlay"""
        cam_w = self.width // 2
        cam_h = self.height // 2
        cam_x = (self.width - cam_w) // 2
        cam_y = (self.height - cam_h) // 2

        surface = self.webcam.get_pygame_surface(cam_w, cam_h)
        if surface:
            self.screen.blit(surface, (cam_x, cam_y))
            # Draw center crop guide box
            margin_x = cam_w // 4
            margin_y = cam_h // 4
            pygame.draw.rect(
                self.screen, (255, 200, 0),
                (cam_x + margin_x, cam_y + margin_y,
                 cam_w - 2 * margin_x, cam_h - 2 * margin_y), 3
            )
        else:
            no_cam = self.ui.font_medium.render("No webcam feed...", True, (255, 100, 100))
            self.screen.blit(no_cam, (self.width // 2 - no_cam.get_width() // 2, self.height // 2))

        self.ui.draw_equation(self.screen, self.current_equation, self.width)
        if self.show_feedback:
            self.ui.draw_feedback(self.screen, self.player_answer, self.correct_answer, self.player_confidence, self.width)
        if self.show_redraw_prompt:
            self.ui.draw_redraw_prompt(self.screen, self.width, self.height)
        self.ui.draw_webcam_instructions(self.screen, self.width, self.height)
        self.ui.draw_round_counter(self.screen, self.battle.round, self.battle.max_rounds, self.width)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()