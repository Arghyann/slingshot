import pygame

class Piglin:
    def __init__(self, screen, backgroundInstance, x, y, side, color=(85, 107, 47   ), durability=1):
        self.screen = screen
        self.background = backgroundInstance
        self.x = x
        self.y = y
        self.width = side
        self.height = side
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.durability = durability
        self.radius=side//2
        #add to background i.e. god
        self.background.piglins.append(self)

    #code of the obstacle to naturally fall to the ground (call it directly in main.py)
    def falling(self):
        # Check if the obstacle is above the ground
        if self.rect.bottom < self.background.grassY:
            # Check if there is an obstacle below
            for entity in self.background.obstacles+self.background.piglins:
                if entity != self:
                    if self.rect.colliderect(entity.rect):
                        if entity.rect.top <= self.rect.bottom:
                            return
            self.y += 1
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect,border_radius=self.radius)


    def is_hit(self):
        self.durability -= 1
        return self.durability <= 0
