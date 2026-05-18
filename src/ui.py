import pygame
import math

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Colors
        self.COLOR_PRIMARY = (200, 220, 255)
        self.COLOR_DARK_BG = (20, 20, 40)
        self.COLOR_ACCENT = (255, 200, 0)
        self.COLOR_SUCCESS = (100, 255, 100)
        self.COLOR_FAIL = (255, 100, 100)
        self.COLOR_PLAYER = (100, 200, 255)
        self.COLOR_ENEMY = (255, 100, 100)
    
    def draw_character(self, screen, x, y, color, is_enemy=False, health_percent=1.0):
        """Draw a simple character (circle with emoji-like features)"""
        # Body
        pygame.draw.circle(screen, color, (x, y), 40)
        
        # Eyes
        eye_offset = 15
        eye_y = y - 10
        pygame.draw.circle(screen, (255, 255, 255), (x - eye_offset, eye_y), 8)
        pygame.draw.circle(screen, (255, 255, 255), (x + eye_offset, eye_y), 8)
        
        # Pupils
        pupil_color = (0, 0, 0)
        pygame.draw.circle(screen, pupil_color, (x - eye_offset, eye_y), 4)
        pygame.draw.circle(screen, pupil_color, (x + eye_offset, eye_y), 4)
        
        # Mouth (happy or sad)
        mouth_y = y + 15
        if health_percent > 0.3:
            # Happy face
            pygame.draw.arc(screen, (0, 0, 0), (x - 15, mouth_y - 5, 30, 15), 0, math.pi, 3)
        else:
            # Sad face
            pygame.draw.arc(screen, (0, 0, 0), (x - 15, mouth_y + 5, 30, 15), math.pi, 2 * math.pi, 3)
    
    def draw_health_bar(self, screen, x, y, width, height, current, maximum, color):
        """Draw an animated health bar"""
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        
        # Health fill
        health_percent = max(0, current / maximum)
        fill_width = width * health_percent
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        
        # Border
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 3)
        
        # Health text
        health_text = f"{int(current)}/{int(maximum)}"
        text = pygame.font.Font(None, 24).render(health_text, True, (255, 255, 255))
        text_x = x + width // 2 - text.get_width() // 2
        text_y = y + height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
    
    def draw_menu(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        
        # Background gradient effect with rects
        for i in range(height):
            color_value = 20 + int((40 * i / height))
            pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, i), (width, i))
        
        title = self.font_large.render("⚔️ Math Battle Game ⚔️", True, self.COLOR_ACCENT)
        subtitle = self.font_small.render("Learn Math Through Combat", True, self.COLOR_PRIMARY)
        start = self.font_medium.render("Press SPACE to Start", True, self.COLOR_PRIMARY)
        
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 4))
        screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, height // 4 + 100))
        screen.blit(start, (width // 2 - start.get_width() // 2, height // 2 + 100))
    
    def draw_chapter_select(self, screen, chapters, unlocked):
        width = screen.get_width()
        
        # Draw background
        for i in range(screen.get_height()):
            color_value = 20 + int((40 * i / screen.get_height()))
            pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, i), (width, i))
        
        title = self.font_large.render("Select Chapter", True, self.COLOR_ACCENT)
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))
        
        for i, chapter in enumerate(chapters):
            y_pos = 200 + i * 100
            color = self.COLOR_PRIMARY if unlocked[i] else (100, 100, 100)
            
            # Chapter box
            box_rect = pygame.Rect(width // 2 - 150, y_pos - 30, 300, 70)
            box_color = self.COLOR_ACCENT if unlocked[i] else (50, 50, 50)
            pygame.draw.rect(screen, box_color, box_rect)
            pygame.draw.rect(screen, color, box_rect, 3)
            
            text = self.font_medium.render(f"{i+1}. {chapter}", True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, y_pos - 20))
            
            if not unlocked[i]:
                locked = self.font_small.render("🔒 Locked", True, (150, 150, 150))
                screen.blit(locked, (width // 2 - locked.get_width() // 2, y_pos + 10))
        
        instruction = self.font_tiny.render("Press SPACE to start", True, self.COLOR_PRIMARY)
        screen.blit(instruction, (width // 2 - instruction.get_width() // 2, screen.get_height() - 80))
    
    def draw_battle(self, screen, battle, width, height):
        """Draw battle screen with characters and health bars"""
        # Enemy at top
        self.draw_character(screen, width // 4, 80, self.COLOR_ENEMY, is_enemy=True, health_percent=battle.enemy_health / 100)
        self.draw_health_bar(screen, width // 4 - 100, 150, 200, 40, battle.enemy_health, 100, self.COLOR_ENEMY)
        
        enemy_label = self.font_small.render("ENEMY", True, self.COLOR_ENEMY)
        screen.blit(enemy_label, (width // 4 - enemy_label.get_width() // 2, 200))
        
        # Player at bottom
        self.draw_character(screen, 3 * width // 4, height - 150, self.COLOR_PLAYER, is_enemy=False, health_percent=battle.player_health / 100)
        self.draw_health_bar(screen, 3 * width // 4 - 100, height - 250, 200, 40, battle.player_health, 100, self.COLOR_PLAYER)
        
        player_label = self.font_small.render("YOU", True, self.COLOR_PLAYER)
        screen.blit(player_label, (3 * width // 4 - player_label.get_width() // 2, height - 100))
    
    def draw_equation(self, screen, equation, width):
        text = self.font_large.render(equation, True, self.COLOR_ACCENT)
        screen.blit(text, (width // 2 - text.get_width() // 2, 40))
    
    def draw_canvas_container(self, screen, x, y, width, height):
        """Draw a styled border around the canvas"""
        pygame.draw.rect(screen, (100, 100, 120), (x - 10, y - 10, width + 20, height + 20))
        pygame.draw.rect(screen, (255, 255, 255), (x - 10, y - 10, width + 20, height + 20), 4)
        
        label = self.font_tiny.render("DRAWING AREA", True, self.COLOR_ACCENT)
        screen.blit(label, (x + width // 2 - label.get_width() // 2, y - 40))
    
    def draw_feedback(self, screen, player_answer, correct_answer, confidence, width):
        """Show feedback on answer submission"""
        correct = (player_answer == correct_answer)
        
        if correct:
            feedback_text = "✓ CORRECT!"
            color = self.COLOR_SUCCESS
        else:
            feedback_text = f"✗ Wrong (You: {player_answer}, Answer: {correct_answer})"
            color = self.COLOR_FAIL
        
        text = self.font_small.render(feedback_text, True, color)
        screen.blit(text, (width // 2 - text.get_width() // 2, 200))
        
        conf_text = self.font_tiny.render(f"Confidence: {confidence * 100:.1f}%", True, self.COLOR_PRIMARY)
        screen.blit(conf_text, (width // 2 - conf_text.get_width() // 2, 260))
    
    def draw_round_counter(self, screen, round_num, max_rounds, width):
        """Draw round indicator"""
        round_text = self.font_small.render(f"Round {round_num}/{max_rounds}", True, self.COLOR_ACCENT)
        screen.blit(round_text, (width - 350, 20))
    
    def draw_instructions(self, screen, width, height):
        instructions = [
            "Draw the answer with your mouse",
            "Press ENTER to submit",
            "Press ESC to quit"
        ]
        for i, text in enumerate(instructions):
            rendered = self.font_tiny.render(text, True, self.COLOR_PRIMARY)
            screen.blit(rendered, (20, height - 100 + i * 30))
    
    def draw_battle_result(self, screen, won, width, height):
        # Draw celebratory/sad overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        if won:
            result_text = "🎉 VICTORY! 🎉"
            color = self.COLOR_SUCCESS
            message = "You defeated the enemy!"
        else:
            result_text = "💀 DEFEAT 💀"
            color = self.COLOR_FAIL
            message = "You were defeated..."
        
        result = self.font_large.render(result_text, True, color)
        msg = self.font_medium.render(message, True, self.COLOR_PRIMARY)
        continue_text = self.font_small.render("Press SPACE to continue", True, self.COLOR_PRIMARY)
        
        screen.blit(result, (width // 2 - result.get_width() // 2, height // 3))
        screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2))
        screen.blit(continue_text, (width // 2 - continue_text.get_width() // 2, 2 * height // 3))
        
    def draw_redraw_prompt(self, screen, width, height):
        text = self.font_medium.render(
        "Can't read that! Please redraw clearly.", 
        True, self.COLOR_ACCENT)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))