import pygame

pygame.init()

class Button:
    def __init__(self, screen, x, y, width, height, text, font=pygame.font.Font(None, 34), color=(125,125,125), hover_color=(255,255,255), text_color=(0,0,0)):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Button Clicked")
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def resetButtonCords(self, pos):
        return self.rect.collidepoint(pos)
    
