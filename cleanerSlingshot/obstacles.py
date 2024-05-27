import pygame

from background import Background

class Obstacle:
    def __init__(self, screen, x, y, width, height, color=(139,69,19), durability=1):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.color = color
        self.durability = durability

    #code of the obstacle to naturally fall to the ground (call it directly in main.py)
    def falling(self):
        # Check if the obstacle is above the ground
        if self.rect.bottom < 400:
            # Check if there is an obstacle below
            for obstacle in Background.obstacles:
                if obstacle != self:
                    if self.rect.colliderect(obstacle.rect):
                        return
            self.y += 1
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def is_hit(self):
        self.durability -= 1
        return self.durability <= 0
