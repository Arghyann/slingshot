import sys
import pygame
from background import Background
from bird import Bird

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Create game objects
    background = Background(screen)
    bird = Bird(screen, mass=40, elasticity=1, cair=2, g=-15, k=2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            bird.handle_events(event)

        bird.update()

        background.draw()
        bird.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
