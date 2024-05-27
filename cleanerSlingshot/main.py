#Created MVP 1.0




import pygame
from background import Background
from bird import Bird

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Angry Birds Simulation")

    background = Background(screen)
    bird = Bird(screen, mass=40, elasticity=1, cair=2, g=-15, k=2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            bird.handle_events(event)

        
        background.draw()
        bird.update()
        bird.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
