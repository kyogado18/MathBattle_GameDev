import os
import sys
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.math_generator import MathGenerator
from src.drawing import DrawingCanvas
from src.battle import BattleSystem
from src.ui import UI

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
        
        self.current_chapter = 0  # 0: addition, 1: subtraction, etc.
        self.chapters = ["Addition", "Subtraction", "Multiplication", "Division"]
        self.unlocked_chapters = [True, False, False, False]  # Start with addition unlocked
        
        self.state = "menu"  # menu, chapter_select, battle, drawing, battle_result
        
        self.current_equation = None
        self.player_answer = None
        self.battle_won = False
        self.player_confidence = 0.0
        self.flash_timer = 0
        self.flash_color = None
        self.show_feedback = False
        self.feedback_timer = 0
        
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
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.state = "chapter_select"
                    elif self.state == "chapter_select":
                        for i, unlocked in enumerate(self.unlocked_chapters):
                            if unlocked:
                                self.current_chapter = i
                                self.start_battle()
                                break
                    elif self.state == "battle_result":
                        self.state = "menu"
                elif event.key == pygame.K_RETURN and self.state == "drawing":
                    self.submit_answer()
            elif self.state == "drawing":
                self.canvas.handle_event(event, self.canvas_x, self.canvas_y)
    
    def update(self):
        self.width, self.height = self.screen.get_size()
        self.canvas_x = (self.width - self.canvas_width) // 2
        self.canvas_y = (self.height - self.canvas_height) // 2
        if self.state == "drawing":
            self.canvas.update()
        
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        else:
            self.show_feedback = False
            # After feedback fades, if waiting for next round, generate new equation
            if self.state == "waiting_for_next_round":
                self.generate_new_equation()
    
    def start_battle(self):
        self.battle = BattleSystem()  # Reset battle
        self.generate_new_equation()
    
    def generate_new_equation(self):
        self.current_equation, self.correct_answer = self.math_gen.generate_equation(self.current_chapter)
        self.state = "drawing"
        self.canvas.clear()
        self.player_answer = None
    
    def submit_answer(self):
        if self.recognizer is not None:
            image_array = self.canvas.get_array()
            result = self.recognizer.predict(image_array)
            if result is None:
                self.player_answer = 0
                self.player_confidence = 0.0
            else:
                digit, confidence = result
                self.player_answer = digit
                self.player_confidence = confidence
            correct = (self.player_answer == self.correct_answer)
        else:
            correct = True
            self.player_answer = self.correct_answer
            self.player_confidence = 1.0
        
        self.show_feedback = True
        self.feedback_timer = 120  # Increased to 120 frames (~2 seconds) to see answer clearly
        
        self.battle.player_attack_enemy(correct)
        if correct:
            self.flash_color = (0, 255, 0)
        else:
            self.flash_color = (255, 0, 0)
        self.flash_timer = 30
        
        if not self.battle.is_battle_over():
            self.battle.enemy_attack_player()
            if not self.battle.is_battle_over():
                # Wait for feedback to finish before generating new equation
                self.state = "waiting_for_next_round"
            else:
                self.battle_won = False
                self.state = "battle_result"
        else:
            if self.current_chapter < 3 and not self.unlocked_chapters[self.current_chapter + 1]:
                self.unlocked_chapters[self.current_chapter + 1] = True
            self.battle_won = True
            self.state = "battle_result"
    
    def draw(self):
        self.screen.fill((20, 20, 40))  # Dark blue background
        
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
        elif self.state == "battle":
            self.ui.draw_battle(self.screen, self.battle, self.width, self.height)
        elif self.state == "drawing" or self.state == "waiting_for_next_round":
            self.ui.draw_equation(self.screen, self.current_equation, self.width)
            self.ui.draw_canvas_container(self.screen, self.canvas_x, self.canvas_y, self.canvas_width, self.canvas_height)
            self.canvas.draw(self.screen, self.canvas_x, self.canvas_y)
            if self.show_feedback:
                self.ui.draw_feedback(self.screen, self.player_answer, self.correct_answer, self.player_confidence, self.width)
            self.ui.draw_instructions(self.screen, self.width, self.height)
            self.ui.draw_round_counter(self.screen, self.battle.round, self.battle.max_rounds, self.width)
        elif self.state == "battle_result":
            self.ui.draw_battle_result(self.screen, self.battle_won, self.width, self.height)
        
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()