#angry birds game
import pygame

pygame.init()


screen = pygame.display.set_mode((800,600))

#bird co-ordinates
bird_x = 111
bird_y = 326

run = True
while run:
    for event in pygame.event.get():

        #event for game close
        if event.type == pygame.QUIT:
            run = False

        #event for mouse clicked on bird\
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bird_x-15 <= pygame.mouse.get_pos()[0] <= bird_x+15 and bird_y-15 <= pygame.mouse.get_pos()[1] <= bird_y+15:
                bird_x, bird_y = pygame.mouse.get_pos()
                print("Mouse Clicked", bird_x, bird_y)
        
    #background
    screen.fill((255,255,255))

    #grass
    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    
    #slingshot
    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))


    #bird
    pygame.draw.circle(screen, (255, 0,0), (bird_x, bird_y), 15)


    pygame.display.flip()