import pygame
import numpy as np

class Bird:
    def __init__(self, screen, mass, elasticity, cair, g, k):
        self.screen = screen
        self.mass = mass
        self.elasticity = elasticity
        self.cair = cair
        self.g = g
        self.k = k
        self.c = cair / mass
        self.g = g / mass
        self.elastic_constant = np.sqrt(k / mass)
        self.bird_radius = 15
        self.original_coords = np.array([111, 323])
        self.current_coords = np.array([111, 323])
        self.bird_held = False
        self.bird_flying = False
        self.u = 0
        self.angle = 0
        self.start_time = 0
        self.time_factor = 20

    def velocity_finder(self, x):
        return self.elastic_constant * x

    def xcord(self, u, s, t):
        # Limit the value of t to avoid overflow issues
        max_t = 1000 / self.time_factor
        t = min(t, max_t)
        return self.original_coords[0] + (u * np.cos(s) / self.c) * (1 - np.exp(-self.c * t))

    def ycord(self, u, s, t):
        # Limit the value of t to avoid overflow issues
        max_t = 1000 / self.time_factor
        t = min(t, max_t)
        term1 = u * np.sin(s) + self.g / self.c
        term2 = (u * np.sin(s) + self.g / self.c) * np.exp(-self.c * t)
        return self.original_coords[1] - ((term1 - term2) / self.c) - self.g * t / self.c

    def vx(self, u, s, t):
        return u * np.exp(-self.c * t)

    def vy(self, u, s, t):
        term = u * self.c + self.g
        return (term * np.exp(-self.c * t) - self.g) * self.c

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_coords[0] - self.bird_radius <= pygame.mouse.get_pos()[0] <= self.current_coords[0] + self.bird_radius and self.current_coords[1] - self.bird_radius <= pygame.mouse.get_pos()[1] <= self.current_coords[1] + self.bird_radius:
                self.bird_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.bird_held = False
            self.current_coords = self.original_coords.copy()
            self.bird_flying = True
            self.start_time = pygame.time.get_ticks() / 1000
            self.u = self.velocity_finder(np.linalg.norm(self.current_coords - self.original_coords))
            self.angle = -np.arctan2(self.original_coords[1] - self.current_coords[1], self.original_coords[0] - self.current_coords[0])

    def update(self):
        if self.bird_held:
            self.current_coords[0], self.current_coords[1] = pygame.mouse.get_pos()
            self.angle = -np.arctan2(self.original_coords[1] - self.current_coords[1], self.original_coords[0] - self.current_coords[0])

        if self.bird_flying:
            t = ((pygame.time.get_ticks() / 1000) - self.start_time) * self.time_factor
            self.current_coords[0] = self.xcord(self.u, self.angle, t)
            self.current_coords[1] = self.ycord(self.u, self.angle, t)

            if self.current_coords[0] + self.bird_radius >= 800:
                self.handle_collision(horizontal=True)
            if self.current_coords[1] + self.bird_radius >= 400:
                self.handle_collision(horizontal=False)

    def handle_collision(self, horizontal):
        t = ((pygame.time.get_ticks() / 1000) - self.start_time) * self.time_factor
        if horizontal:
            new_vx = -self.vx(self.u, self.angle, t)
            new_vy = -self.vy(self.u, self.angle, t)
            self.u = -self.elasticity * np.linalg.norm([new_vx, new_vy])
            self.angle = np.arctan2(new_vy, new_vx)
            self.original_coords[0] = 800 - self.bird_radius
        else:
            new_vx = self.vx(self.u, self.angle, t)
            new_vy = -self.vy(self.u, self.angle, t)
            self.u = 50 * np.linalg.norm([new_vy, new_vx])
            self.angle = -np.arctan(new_vy / new_vx)
            self.current_coords[1] = 400 - self.bird_radius - 1

        self.original_coords = self.current_coords.copy()
        self.start_time = pygame.time.get_ticks() / 1000

    def draw(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.current_coords[0]), int(self.current_coords[1])), self.bird_radius)
