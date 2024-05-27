#Created MVP 1.4




import pygame
from piglins import Piglin
from background import Background
from bird import Bird
from obstacles import Obstacle

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Angry Birds Simulation")

    background = Background(screen)
    bird = Bird(screen, background, mass=40, elasticity=1, cair=2, g=-20, k=2)

    Obstacle(screen, background, x=400, y=300, width=20, height=100)
    Obstacle(screen, background, x=500, y=300, width=20, height=100)
    Obstacle(screen, background, x=400, y=280, width=120, height=20)

    Piglin(screen, background, x=430, y=240, side=40)



    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            bird.handle_events(event)

        
        background.draw()
        bird.reset()
        bird.update()
        bird.draw()

        for obstacle in background.obstacles:
            obstacle.falling()
            obstacle.draw()

        for piglin in background.piglins:
            piglin.falling()
            piglin.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
