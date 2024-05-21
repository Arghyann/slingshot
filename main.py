import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))

run = True
while run:
    for event in pygame.event.get():

        #event for game close
        if event.type == pygame.QUIT:
            run = False

        #event for mouse clicked on bird\
        if event.type == pygame.MOUSEBUTTONDOWN and (110, 320) <= pygame.mouse.get_pos() <= (125, 335):
            print("Mouse Clicked")
        
    
    screen.fill((255,255,255))

    #grass
    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    
    #slingshot
    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))


    #bird
    pygame.draw.circle(screen, (255, 0,0), (110, 320), 15)


    pygame.display.flip()