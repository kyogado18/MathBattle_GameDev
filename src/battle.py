import pygame

class BattleSystem:
    def __init__(self):
        self.player_health = 100
        self.enemy_health = 100
        self.player_attack = 20
        self.enemy_attack = 15
        self.round = 0
        self.max_rounds = 5
    
    def player_attack_enemy(self, correct):
        if correct:
            damage = self.player_attack
        else:
            damage = self.player_attack // 2
        self.enemy_health -= damage
        if self.enemy_health < 0:
            self.enemy_health = 0
        self.round += 1
    
    def enemy_attack_player(self):
        self.player_health -= self.enemy_attack
        if self.player_health < 0:
            self.player_health = 0
    
    def is_battle_over(self):
        return self.player_health <= 0 or self.enemy_health <= 0
    
    def draw(self, screen):
        # Simple battle UI
        font = pygame.font.Font(None, 36)
        
        player_text = font.render(f"Player: {self.player_health}", True, (0, 0, 0))
        enemy_text = font.render(f"Enemy: {self.enemy_health}", True, (0, 0, 0))
        
        screen.blit(player_text, (50, 50))
        screen.blit(enemy_text, (600, 50))
        
        # Draw health bars
        pygame.draw.rect(screen, (0, 255, 0), (50, 80, self.player_health * 2, 20))
        pygame.draw.rect(screen, (255, 0, 0), (600, 80, self.enemy_health * 2, 20))