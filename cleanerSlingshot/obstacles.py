import pygame

class Obstacle:
    def __init__(self, screen, x, y, width, height, color=(139,69,19), durability=1):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.durability = durability
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def is_hit(self):
        self.durability -= 1
        return self.durability <= 0
