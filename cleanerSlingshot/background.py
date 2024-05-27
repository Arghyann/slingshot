import pygame

class Background:
    def __init__(self,x=800,y=600):
        self.x=x
        self.y=y
        self.screen =pygame.display.set_mode((self.x,self.y))
        self.obstacles = []
        self.piglins = []
        self.grassY=400

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw grass
        pygame.draw.rect(self.screen, (0, 255, 0), (0, self.grassY,self.x, 200))
        # Draw slingshot
        pygame.draw.rect(self.screen, (120, 0, 150), (100, 340, 20, 60))
