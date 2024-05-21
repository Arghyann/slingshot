import pygame



pygame.init()


screen = pygame.display.set_mode((800,600))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((255,255,255))

    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))

    pygame.display.flip()