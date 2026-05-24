import pygame
import math

class UI:
    def __init__(self):
        self.font_path = "assets/fonts/NTBrickSans.ttf"
        self.menu_bg_path = "assets/images/mathbattle background.png"
        self.title_image_path = "assets/ui/mathbattle title text img.png"

        self.font_large = pygame.font.Font(self.font_path, 72)
        self.font_medium = pygame.font.Font(self.font_path, 48)
        self.font_small = pygame.font.Font(self.font_path, 32)
        self.font_tiny = pygame.font.Font(self.font_path, 24)
        
        # Preload menu images
        try:
            self.menu_background = pygame.image.load(self.menu_bg_path).convert()
        except Exception:
            self.menu_background = None
        try:
            self.title_image = pygame.image.load(self.title_image_path).convert_alpha()
        except Exception:
            self.title_image = None

        self.chapter_title_image_path = "assets/ui/mathbattle_selectchapter_text.png"
        self.battle_bg_path = "assets/images/battle_background.png"
        try:
            self.chapter_title_image = pygame.image.load(self.chapter_title_image_path).convert_alpha()
        except Exception:
            self.chapter_title_image = None
        try:
            self.battle_background = pygame.image.load(self.battle_bg_path).convert()
        except Exception:
            self.battle_background = None
        
        # Colors
        self.COLOR_PRIMARY = (200, 220, 255)
        self.OUTLINE_COLOR = (10, 10, 10)

    def _is_light_color(self, color):
        r, g, b = color
        return (r + g + b) / 3 > 128

    def draw_text(self, screen, font, text, color, pos, outline_exclude=False):
        text_surface = font.render(text, True, color)
        if not outline_exclude and self._is_light_color(color) and "Locked" not in text:
            outline_surface = font.render(text, True, self.OUTLINE_COLOR)
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for ox, oy in offsets:
                screen.blit(outline_surface, (pos[0] + ox, pos[1] + oy))
        screen.blit(text_surface, pos)
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
        text_font = pygame.font.Font(None, 24)
        text_x = x + width // 2 - text_font.size(health_text)[0] // 2
        text_y = y + height // 2 - text_font.size(health_text)[1] // 2
        self.draw_text(screen, text_font, health_text, (255, 255, 255), (text_x, text_y))
    
    def draw_menu(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        
        if self.menu_background:
            bg = pygame.transform.scale(self.menu_background, (width, height))
            screen.blit(bg, (0, 0))
        else:
            # Background gradient effect with rects
            for i in range(height):
                color_value = 20 + int((40 * i / height))
                pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, i), (width, i))

        if self.title_image:
            max_title_width = int(width * 0.75)
            max_title_height = int(height * 0.18)
            title = self.title_image
            title_w, title_h = title.get_size()

            scale_ratio = min(1.0, max_title_width / title_w, max_title_height / title_h)
            if scale_ratio < 1.0:
                title = pygame.transform.smoothscale(
                    title,
                    (int(title_w * scale_ratio), int(title_h * scale_ratio))
                )

            title_x = width // 2 - title.get_width() // 2
            title_y = height // 4 - title.get_height() // 2
            screen.blit(title, (title_x, title_y))
        else:
            title_text = "⚔️ Math Battle Game ⚔️"
            title_pos = (width // 2 - self.font_large.size(title_text)[0] // 2, height // 4)
            self.draw_text(screen, self.font_large, title_text, self.COLOR_ACCENT, title_pos)

        subtitle_text = "Learn Math Through Combat"
        start_text = "Press SPACE to Start"
        subtitle_pos = (width // 2 - self.font_small.size(subtitle_text)[0] // 2, height // 4 + 100)
        start_pos = (width // 2 - self.font_medium.size(start_text)[0] // 2, height // 2 + 100)
        self.draw_text(screen, self.font_small, subtitle_text, self.COLOR_PRIMARY, subtitle_pos)
        self.draw_text(screen, self.font_medium, start_text, self.COLOR_PRIMARY, start_pos)
    
    def draw_chapter_select(self, screen, chapters, unlocked):
        width = screen.get_width()
        height = screen.get_height()

        if self.menu_background:
            bg = pygame.transform.scale(self.menu_background, (width, height))
            screen.blit(bg, (0, 0))
        else:
            for i in range(height):
                color_value = 20 + int((40 * i / height))
                pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, i), (width, i))

        if self.chapter_title_image:
            max_title_width = int(width * 0.75)
            max_title_height = int(height * 0.12)
            title = self.chapter_title_image
            title_w, title_h = title.get_size()
            scale_ratio = min(1.0, max_title_width / title_w, max_title_height / title_h)
            if scale_ratio < 1.0:
                title = pygame.transform.smoothscale(
                    title,
                    (int(title_w * scale_ratio), int(title_h * scale_ratio))
                )

            title_x = width // 2 - title.get_width() // 2
            title_y = int(height * 0.08)
            screen.blit(title, (title_x, title_y))
            content_top = title_y + title.get_height() + 30
        else:
            title_font = pygame.font.Font(self.font_path, max(40, min(64, int(width * 0.05))))
            title_text = "Select Chapter"
            title_pos = (width // 2 - title_font.size(title_text)[0] // 2, 50)
            self.draw_text(screen, title_font, title_text, self.COLOR_ACCENT, title_pos)
            content_top = 130

        chapter_font = pygame.font.Font(self.font_path, max(28, min(42, int(width * 0.035))))
        info_font = pygame.font.Font(self.font_path, max(18, min(28, int(width * 0.03))))
        instruction_font = pygame.font.Font(self.font_path, max(18, min(26, int(width * 0.025))))

        for i, chapter in enumerate(chapters):
            y_pos = content_top + i * (int(height * 0.12))
            color = self.COLOR_PRIMARY if unlocked[i] else (180, 180, 180)

            box_width = int(width * 0.6)
            box_height = int(height * 0.1)
            box_rect = pygame.Rect(width // 2 - box_width // 2, y_pos, box_width, box_height)
            box_color = self.COLOR_ACCENT if unlocked[i] else (50, 50, 50)
            pygame.draw.rect(screen, box_color, box_rect, border_radius=12)
            pygame.draw.rect(screen, color, box_rect, 3, border_radius=12)

            chapter_text = f"{i + 1}. {chapter}"
            chapter_pos = (width // 2 - chapter_font.size(chapter_text)[0] // 2, y_pos + 10)
            self.draw_text(screen, chapter_font, chapter_text, color, chapter_pos)

            if not unlocked[i]:
                locked_text = "🔒 Locked"
                locked_pos = (width // 2 - info_font.size(locked_text)[0] // 2, y_pos + box_height - info_font.size(locked_text)[1] - 10)
                self.draw_text(screen, info_font, locked_text, (220, 220, 220), locked_pos, outline_exclude=True)

        instruction_text = "Press SPACE to start"
        instruction_pos = (width // 2 - instruction_font.size(instruction_text)[0] // 2, height - 80)
        self.draw_text(screen, instruction_font, instruction_text, self.COLOR_PRIMARY, instruction_pos)
    
    def draw_battle(self, screen, battle, width, height):
        """Draw battle screen with characters and health bars"""
        if self.battle_background:
            bg = pygame.transform.scale(self.battle_background, (width, height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill(self.COLOR_DARK_BG)

        # Dynamic fonts for battle labels
        label_size = max(24, min(42, int(width * 0.03)))
        label_font = pygame.font.Font(self.font_path, label_size)

        # Enemy at top
        self.draw_character(screen, width // 4, 80, self.COLOR_ENEMY, is_enemy=True, health_percent=battle.enemy_health / 100)
        self.draw_health_bar(screen, width // 4 - 100, 150, 200, 40, battle.enemy_health, 100, self.COLOR_ENEMY)
        
        enemy_text = "ENEMY"
        enemy_pos = (width // 4 - label_font.size(enemy_text)[0] // 2, 200)
        self.draw_text(screen, label_font, enemy_text, self.COLOR_ENEMY, enemy_pos)
        
        # Player at bottom
        self.draw_character(screen, 3 * width // 4, height - 150, self.COLOR_PLAYER, is_enemy=False, health_percent=battle.player_health / 100)
        self.draw_health_bar(screen, 3 * width // 4 - 100, height - 250, 200, 40, battle.player_health, 100, self.COLOR_PLAYER)
        
        player_text = "YOU"
        player_pos = (3 * width // 4 - label_font.size(player_text)[0] // 2, height - 100)
        self.draw_text(screen, label_font, player_text, self.COLOR_PLAYER, player_pos)

    def draw_equation(self, screen, equation, width):
        font_size = max(40, min(80, int(width * 0.055)))
        equation_font = pygame.font.Font(self.font_path, font_size)
        text_pos = (width // 2 - equation_font.size(equation)[0] // 2, 40)
        self.draw_text(screen, equation_font, equation, self.COLOR_ACCENT, text_pos)

    def draw_canvas_container(self, screen, x, y, width, height, eraser_mode=False):
        """Draw a styled border around the canvas"""
        color = (255, 150, 50) if eraser_mode else (255, 255, 255)
        pygame.draw.rect(screen, (100, 100, 120), (x - 10, y - 10, width + 20, height + 20))
        pygame.draw.rect(screen, color, (x - 10, y - 10, width + 20, height + 20), 4)

        mode_label = "ERASER MODE" if eraser_mode else "DRAWING AREA"
        label_pos = (x + width // 2 - self.font_tiny.size(mode_label)[0] // 2, y - 40)
        self.draw_text(screen, self.font_tiny, mode_label, self.COLOR_ACCENT, label_pos)

    def draw_feedback(self, screen, player_answer, correct_answer, confidence, width):
        """Show feedback on answer submission"""
        correct = (player_answer == correct_answer)
        
        if correct:
            feedback_text = "✓ CORRECT!"
            color = self.COLOR_SUCCESS
        else:
            feedback_text = f"✗ Wrong (You: {player_answer}, Answer: {correct_answer})"
            color = self.COLOR_FAIL
        
        feedback_pos = (width // 2 - self.font_small.size(feedback_text)[0] // 2, 200)
        self.draw_text(screen, self.font_small, feedback_text, color, feedback_pos)
        
        conf_text_str = f"Confidence: {confidence * 100:.1f}%"
        conf_pos = (width // 2 - self.font_tiny.size(conf_text_str)[0] // 2, 260)
        self.draw_text(screen, self.font_tiny, conf_text_str, self.COLOR_PRIMARY, conf_pos)
    
    def draw_round_counter(self, screen, round_num, max_rounds, width):
        """Draw round indicator"""
        round_text = f"Round {round_num}/{max_rounds}"
        round_pos = (width - 350, 20)
        self.draw_text(screen, self.font_small, round_text, self.COLOR_ACCENT, round_pos)
    
    def draw_instructions(self, screen, width, height):
        # instructions = [
        #     "Draw the answer with your mouse",
        #     "Press ENTER to submit",
        #     "Press ESC to quit"
        # ]
        # for i, text in enumerate(instructions):
        #     rendered = self.font_tiny.render(text, True, self.COLOR_PRIMARY)
        #     screen.blit(rendered, (20, height - 100 + i * 30))

        # Show eraser status
        instructions = [
            "Draw answer | ENTER to submit | ESC to exit",
            "E = toggle eraser | C = clear canvas",
        ]
        for i, text in enumerate(instructions):
            self.draw_text(screen, self.font_tiny, text, self.COLOR_PRIMARY, (20, height - 70 + i * 30))
        
    
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
        
        result_pos = (width // 2 - self.font_large.size(result_text)[0] // 2, height // 3)
        self.draw_text(screen, self.font_large, result_text, color, result_pos)
        msg_pos = (width // 2 - self.font_medium.size(message)[0] // 2, height // 2)
        self.draw_text(screen, self.font_medium, message, self.COLOR_PRIMARY, msg_pos)
        continue_text = "Press SPACE to continue"
        continue_pos = (width // 2 - self.font_small.size(continue_text)[0] // 2, 2 * height // 3)
        self.draw_text(screen, self.font_small, continue_text, self.COLOR_PRIMARY, continue_pos)
        
    def draw_redraw_prompt(self, screen, width, height):
        text = "Can't read that! Please redraw clearly."
        pos = (width // 2 - self.font_medium.size(text)[0] // 2, height // 2)
        self.draw_text(screen, self.font_medium, text, self.COLOR_ACCENT, pos)

    def draw_input_select(self, screen, equation, width, height):
        """Input method selection screen shown before every round"""
        if self.battle_background:
            bg = pygame.transform.scale(self.battle_background, (width, height))
            screen.blit(bg, (0, 0))
        else:
            screen.fill(self.COLOR_DARK_BG)

        # Draw equation at top
        self.draw_equation(screen, equation, width)

        title_size = max(32, min(56, int(width * 0.045)))
        button_size = max(24, min(36, int(width * 0.03)))
        subtitle_size = max(18, min(28, int(width * 0.025)))
        hint_size = max(16, min(24, int(width * 0.02)))

        title_font = pygame.font.Font(self.font_path, title_size)
        button_font = pygame.font.Font(self.font_path, button_size)
        sub_font = pygame.font.Font(self.font_path, subtitle_size)
        hint_font = pygame.font.Font(self.font_path, hint_size)

        title_text = "Choose Input Method"
        title_y = int(height * 0.28)
        title_pos = (width // 2 - title_font.size(title_text)[0] // 2, title_y)
        self.draw_text(screen, title_font, title_text, self.COLOR_ACCENT, title_pos)

        button_width = int(width * 0.28)
        button_height = int(height * 0.12)
        button_spacing = int(width * 0.04)
        button_top = int(height * 0.42)

        # Canvas button
        canvas_rect = pygame.Rect(width // 2 - button_width - button_spacing // 2, button_top, button_width, button_height)
        pygame.draw.rect(screen, (40, 80, 120), canvas_rect, border_radius=14)
        pygame.draw.rect(screen, self.COLOR_PLAYER, canvas_rect, 3, border_radius=14)
        canvas_text_str = "1. Drawing"
        canvas_sub_str = "Use mouse/trackpad"
        canvas_text_pos = (canvas_rect.centerx - button_font.size(canvas_text_str)[0] // 2, canvas_rect.y + int(button_height * 0.18))
        canvas_sub_pos = (canvas_rect.centerx - sub_font.size(canvas_sub_str)[0] // 2, canvas_rect.y + int(button_height * 0.55))
        self.draw_text(screen, button_font, canvas_text_str, self.COLOR_PLAYER, canvas_text_pos)
        self.draw_text(screen, sub_font, canvas_sub_str, self.COLOR_PRIMARY, canvas_sub_pos)

        # Webcam button
        webcam_rect = pygame.Rect(width // 2 + button_spacing // 2, button_top, button_width, button_height)
        pygame.draw.rect(screen, (40, 100, 60), webcam_rect, border_radius=14)
        pygame.draw.rect(screen, self.COLOR_SUCCESS, webcam_rect, 3, border_radius=14)
        webcam_text_str = "2. Webcam"
        webcam_sub_str = "Hold up your answer"
        webcam_text_pos = (webcam_rect.centerx - button_font.size(webcam_text_str)[0] // 2, webcam_rect.y + int(button_height * 0.18))
        webcam_sub_pos = (webcam_rect.centerx - sub_font.size(webcam_sub_str)[0] // 2, webcam_rect.y + int(button_height * 0.55))
        self.draw_text(screen, button_font, webcam_text_str, self.COLOR_SUCCESS, webcam_text_pos)
        self.draw_text(screen, sub_font, webcam_sub_str, self.COLOR_PRIMARY, webcam_sub_pos)

        hint_str = "Click a button or press 1 / 2"
        hint_pos = (width // 2 - hint_font.size(hint_str)[0] // 2, button_top + button_height + int(height * 0.05))
        self.draw_text(screen, hint_font, hint_str, self.COLOR_PRIMARY, hint_pos)

    def draw_webcam_instructions(self, screen, width, height):
        # instructions = [
        #     "Hold up your written answer inside the box",
        #     "Press ENTER to capture",
        #     "Press ESC to go back"
        # ]
        # for i, text in enumerate(instructions):
        #     rendered = self.font_tiny.render(text, True, self.COLOR_PRIMARY)
        #     screen.blit(rendered, (20, height - 100 + i * 30))

        instructions = [
        "Hold answer inside the yellow box | ENTER to capture",
        "F = flip camera | ESC to go back",
        ]
        for i, text in enumerate(instructions):
            self.draw_text(screen, self.font_tiny, text, self.COLOR_PRIMARY, (20, height - 70 + i * 30))

    def draw_webcam_warning(self, screen, correct, attempts, width, height):
        """Low accuracy warning screen"""
        accuracy = (correct / attempts * 100) if attempts > 0 else 0

        # Dark overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Warning box
        box_rect = pygame.Rect(width // 2 - 300, height // 2 - 150, 600, 300)
        pygame.draw.rect(screen, (40, 30, 10), box_rect, border_radius=16)
        pygame.draw.rect(screen, self.COLOR_ACCENT, box_rect, 3, border_radius=16)

        title_text = "Low Accuracy Warning"
        title_pos = (width // 2 - self.font_medium.size(title_text)[0] // 2, height // 2 - 130)
        self.draw_text(screen, self.font_medium, title_text, self.COLOR_ACCENT, title_pos)

        stat_text = f"Webcam accuracy: {correct}/{attempts} ({accuracy:.0f}%)"
        stat_pos = (width // 2 - self.font_small.size(stat_text)[0] // 2, height // 2 - 70)
        self.draw_text(screen, self.font_small, stat_text, self.COLOR_FAIL, stat_pos)

        suggestion_text = "Consider switching to the drawing canvas."
        suggestion_pos = (width // 2 - self.font_small.size(suggestion_text)[0] // 2, height // 2 - 20)
        self.draw_text(screen, self.font_small, suggestion_text, self.COLOR_PRIMARY, suggestion_pos)

        enter_text = "Press ENTER to switch to canvas"
        enter_pos = (width // 2 - self.font_tiny.size(enter_text)[0] // 2, height // 2 + 50)
        self.draw_text(screen, self.font_tiny, enter_text, self.COLOR_SUCCESS, enter_pos)
        space_text = "Press SPACE to continue with webcam anyway"
        space_pos = (width // 2 - self.font_tiny.size(space_text)[0] // 2, height // 2 + 85)
        self.draw_text(screen, self.font_tiny, space_text, (180, 180, 180), space_pos)

    def draw_redraw_prompt(self, screen, width, height):
        text = "Can't read that! Please try again."
        pos = (width // 2 - self.font_medium.size(text)[0] // 2, height // 2 + 200)
        self.draw_text(screen, self.font_medium, text, self.COLOR_ACCENT, pos)