import pygame

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw_menu(self, screen):
        title = self.font_large.render("Math Battle Game", True, (0, 0, 0))
        start = self.font_medium.render("Press SPACE to Start", True, (0, 0, 0))
        
        screen.blit(title, (400 - title.get_width() // 2, 200))
        screen.blit(start, (400 - start.get_width() // 2, 300))
    
    def draw_chapter_select(self, screen, chapters, unlocked):
        title = self.font_large.render("Select Chapter", True, (0, 0, 0))
        screen.blit(title, (400 - title.get_width() // 2, 100))
        
        for i, chapter in enumerate(chapters):
            color = (0, 0, 0) if unlocked[i] else (128, 128, 128)
            text = self.font_medium.render(f"{i+1}. {chapter}", True, color)
            screen.blit(text, (400 - text.get_width() // 2, 200 + i * 50))
        
        instruction = self.font_small.render("Press SPACE to start the first unlocked chapter", True, (0, 0, 0))
        screen.blit(instruction, (400 - instruction.get_width() // 2, 450))
    
    def draw_equation(self, screen, equation):
        text = self.font_large.render(equation, True, (0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 50))
    
    def draw_instructions(self, screen):
        instructions = [
            "Draw the answer with your mouse",
            "Press ENTER to submit"
        ]
        for i, text in enumerate(instructions):
            rendered = self.font_small.render(text, True, (0, 0, 0))
            screen.blit(rendered, (50, 500 + i * 30))
    
    def draw_battle_result(self, screen, won):
        if won:
            result_text = "You Won!"
            color = (0, 255, 0)
        else:
            result_text = "You Lost!"
            color = (255, 0, 0)
        
        result = self.font_large.render(result_text, True, color)
        continue_text = self.font_medium.render("Press SPACE to continue", True, (0, 0, 0))
        
        screen.blit(result, (400 - result.get_width() // 2, 250))
        screen.blit(continue_text, (400 - continue_text.get_width() // 2, 350))