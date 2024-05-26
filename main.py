#angry birds game
import sys
import pygame
import numpy as np
pygame.init()
time=pygame.time.Clock()
elasticity=0.5
cair=2              
mass=40
c=cair/mass
g=-15/mass  #because of the stupid coordinate system in pygame (why would you let origin be the top left corner)
k=2
x=1              #distance pulled
elastic_constant=np.sqrt(k/mass)
u=0
angle=0

t=0
time_factor=50 #to speed up the simulation
def velocity_finder(xi):
    return elastic_constant*xi       #how much you pull it back->x
def xcord(u,s,z):                                   #u and s are the speeds and the angles
    
    return originalcords[0]+(u * (np.cos(s)) / c) * (1 - np.exp(-c * z))
    
def ycord(u,s,z):
    term1 = u * (np.sin(s)) + g / c
    term2 = (u * (np.sin(s)) + g / c) * np.exp(-c * z)
    
    return originalcords[1]-((term1 - term2) / c) - g * t / c
def vx(u,s,t):
    return u*np.exp(-c*t)
def vy(u,s,t):
    term=u*c+g
    return (term*np.exp(-c*t) - g)*c
screen = pygame.display.set_mode((800,600))
def draw_projection():
        
    points = []
    drawtime=pygame.time.get_ticks() / 1000
    for i in range(1,500):
                z = ((pygame.time.get_ticks() / 1000)-drawtime)*time_factor*i  # Incremental time for projection
                print(u,angle)
                x = xcord(u, angle, z)
                y = ycord(u, angle, z)
                
                points.append((int(x), int(y)))
    if len(points) > 1:
                pygame.draw.lines(screen, (0, 0, 0), False, points, 1)
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
                

        if event.type == pygame.MOUSEBUTTONUP:
            birdHeld = False
            currentcords=originalcords.copy()  #updates before birdflying is updated DO NOT CHANGE
            print("Mouse Released")
            BirdFlying=True
            startTime=pygame.time.get_ticks() / 1000
            
            print("u", u,"angle", np.degrees(angle))

    if birdHeld:
        currentcords[0], currentcords[1] = pygame.mouse.get_pos()
        x=np.linalg.norm(currentcords-originalcords)         #displays x
        angle = -(np.arctan2(originalcords[1] - currentcords[1], originalcords[0] - currentcords[0]))       #edit it so that it outputs negative 
        u=velocity_finder(x)
        startTime=pygame.time.get_ticks() / 1000
        t=((pygame.time.get_ticks() / 1000) - startTime) * time_factor
        print("bird held:", birdHeld)
        
        
    if currentcords[0] + birdRadius <= 800 and currentcords[1]+birdRadius<=400 and BirdFlying:       
        t = ((pygame.time.get_ticks() / 1000) - startTime) * time_factor
        currentcords[0] = xcord(u, angle, t)
        currentcords[1] = ycord(u, angle, t)
            
        
            
            
    
        
    if (currentcords[0] + birdRadius >= 800) and BirdFlying:        # When it flies out of the frame
        print("updated u and angle after collision")
        print("current cords here", currentcords)
          # Elasticity is 1
        newvx=-vx(u,angle,t)
        newvy=-vy(-u,angle,t)
        u=-elasticity*np.linalg.norm([newvx,newvy])
        angle=np.arctan2(newvy,newvx)

        originalcords=[800-birdRadius,currentcords[1]]
        currentcords=originalcords.copy()
        
       
        startTime=pygame.time.get_ticks() /1000

    if currentcords[1]+birdRadius>+400:
        BirdFlying=False
    
    screen.fill((255,255,255))
    
    #grass
    pygame.draw.rect(screen, (0,255,0), (0, 400, 800, 200))

    
    #slingshot
    pygame.draw.rect(screen, (120,0,150), (100,340, 20, 60))


    #bird
    
    pygame.draw.circle(screen, (255, 0,0), (currentcords[0], currentcords[1]), birdRadius)

    if birdHeld: draw_projection()
    pygame.display.flip()