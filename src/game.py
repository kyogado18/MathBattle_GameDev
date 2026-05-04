import pygame
from src.math_generator import MathGenerator
from src.drawing import DrawingCanvas
# from src.recognition import DigitRecognizer  # Temporarily disabled
from src.battle import BattleSystem
from src.ui import UI

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Math Battle Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.math_gen = MathGenerator()
        self.canvas = DrawingCanvas(400, 300)
        # self.recognizer = DigitRecognizer()  # Temporarily disabled
        self.battle = BattleSystem()
        self.ui = UI()
        
        self.current_chapter = 0  # 0: addition, 1: subtraction, etc.
        self.chapters = ["Addition", "Subtraction", "Multiplication", "Division"]
        self.unlocked_chapters = [True, False, False, False]  # Start with addition unlocked
        
        self.state = "menu"  # menu, chapter_select, battle, drawing, battle_result
        
        self.current_equation = None
        self.player_answer = None
        self.battle_won = False
        
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
                if event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.state = "chapter_select"
                    elif self.state == "chapter_select":
                        # Select the first unlocked chapter
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
                self.canvas.handle_event(event)
    
    def update(self):
        if self.state == "drawing":
            self.canvas.update()
    
    def start_battle(self):
        self.state = "battle"
        self.battle = BattleSystem()  # Reset battle
        self.generate_new_equation()
    
    def generate_new_equation(self):
        self.current_equation, self.correct_answer = self.math_gen.generate_equation(self.current_chapter)
        self.state = "drawing"
        self.canvas.clear()
        self.player_answer = None
    
    def submit_answer(self):
        # For now, assume the answer is correct for testing
        # image_array = self.canvas.get_array()
        # digit, confidence = self.recognizer.predict(image_array)
        # self.player_answer = digit
        # correct = (self.player_answer == self.correct_answer)
        correct = True  # Dummy correct
        self.player_answer = self.correct_answer  # Dummy
        
        self.battle.player_attack_enemy(correct)
        if not self.battle.is_battle_over():
            self.battle.enemy_attack_player()
            if not self.battle.is_battle_over():
                self.generate_new_equation()
            else:
                # Player lost
                self.battle_won = False
                self.state = "battle_result"
        else:
            # Player won the battle
            if self.current_chapter < 3 and not self.unlocked_chapters[self.current_chapter + 1]:
                self.unlocked_chapters[self.current_chapter + 1] = True
            self.battle_won = True
            self.state = "battle_result"
    
    def draw(self):
        self.screen.fill((255, 255, 255))
        
        if self.state == "menu":
            self.ui.draw_menu(self.screen)
        elif self.state == "chapter_select":
            self.ui.draw_chapter_select(self.screen, self.chapters, self.unlocked_chapters)
        elif self.state == "battle":
            self.battle.draw(self.screen)
        elif self.state == "drawing":
            self.ui.draw_equation(self.screen, self.current_equation)
            self.canvas.draw(self.screen, 200, 150)
            self.ui.draw_instructions(self.screen)
        elif self.state == "battle_result":
            self.ui.draw_battle_result(self.screen, self.battle_won)
        
        pygame.display.flip()