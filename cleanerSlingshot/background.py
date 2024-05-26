import pygame

class Background:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.fill((255, 255, 255))
        # Draw grass
        pygame.draw.rect(self.screen, (0, 255, 0), (0, 400, 800, 200))
        # Draw slingshot
        pygame.draw.rect(self.screen, (120, 0, 150), (100, 340, 20, 60))
