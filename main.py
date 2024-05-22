#angry birds game
import pygame
import numpy as np
pygame.init()
time=pygame.time.Clock()
cair=2                   
mass=4
c=cair/mass
g=9.8/mass
k=2
x=1              #distance pulled
elastic_constant=np.sqrt(k/mass)
u=0
angle=0
def velocity_finder(xi):
    return elastic_constant*xi       #how much you pull it back->x
def xcord(u,s,t):                                   #u and s are the speeds and the angles
    return originalcords[0]+(u * (np.cos(s)) / c) * (1 - np.exp(-c * t))
def ycord(u,s,t):
    term1 = u * (np.sin(s)) + g / c
    term2 = (u * (np.sin(s)) + g / c) * np.exp(-c * t)
    return originalcords[1]-((term1 - term2) / c) - g * t / c
screen = pygame.display.set_mode((800,600))

#bird co-ordinates
originalcords=np.array([111,323])
currentcords=np.array([111,323])
birdRadius = 15
birdHeld = False
BirdFlying=False
run = True
while run:
    for event in pygame.event.get():

        #event for game close
        if event.type == pygame.QUIT:
            run = False

        #event for mouse clicked on bird
        if event.type == pygame.MOUSEBUTTONDOWN:
            if currentcords[0] - birdRadius <= pygame.mouse.get_pos()[0] <= currentcords[0]+birdRadius and currentcords[1]-birdRadius <= pygame.mouse.get_pos()[1] <= currentcords[1]+birdRadius:
                birdHeld = True
                print("Mouse Clicked")

        if event.type == pygame.MOUSEBUTTONUP:
            birdHeld = False
            print("Mouse Released")
            BirdFlying=True
            startTime=pygame.time.get_ticks() / 1000
            u=velocity_finder(x)
            print("u", u,"angle", angle)

    if birdHeld:
        currentcords[0], currentcords[1] = pygame.mouse.get_pos()
        x=np.linalg.norm(currentcords-originalcords)         #displays x
        angle = np.arctan2(originalcords[1] - currentcords[1], originalcords[0] - currentcords[0])       #edit it so that it outputs negative 
        print("New Cords distance: ",x)
    if BirdFlying:
        t=(pygame.time.get_ticks() / 1000)-startTime
        currentcords[0]=xcord(u,angle,t)
        currentcords[1]=ycord(u,angle,t)

    #background
    screen.fill((255,255,255))

    #grass
    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    
    #slingshot
    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))


    #bird
    pygame.draw.circle(screen, (255, 0,0), (currentcords[0], currentcords[1]), birdRadius)


    pygame.display.flip()