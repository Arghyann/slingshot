#angry birds game
import pygame

pygame.init()


screen = pygame.display.set_mode((800,600))

#bird co-ordinates
birdX = 111
birdY = 323
birdRadius = 15
birdHeld = False

run = True
while run:
    for event in pygame.event.get():

        #event for game close
        if event.type == pygame.QUIT:
            run = False

        #event for mouse clicked on bird
        if event.type == pygame.MOUSEBUTTONDOWN:
            if birdX - birdRadius <= pygame.mouse.get_pos()[0] <= birdX+birdRadius and birdY-birdRadius <= pygame.mouse.get_pos()[1] <= birdY+birdRadius:
                birdHeld = True
                print("Mouse Clicked")

        if event.type == pygame.MOUSEBUTTONUP:
            birdHeld = False
            print("Mouse Released")
    
    if birdHeld:
        birdX, birdY = pygame.mouse.get_pos()
        print("New Cords: ", birdX, birdY)
        
    #background
    screen.fill((255,255,255))

    #grass
    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    
    #slingshot
    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))


    #bird
    pygame.draw.circle(screen, (255, 0,0), (birdX, birdY), birdRadius)


    pygame.display.flip()