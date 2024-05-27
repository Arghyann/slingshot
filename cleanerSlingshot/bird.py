import pygame
import numpy as np
from button import Button
from background import Background

class Bird:
    def __init__(self, screen, backgroundInstance, mass, elasticity, cair, g, k):
        self.screen = screen
        self.background = backgroundInstance
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
        self.min_velocity_threshold = 10 # Minimum velocity threshold to stop the bird

        #self.rect = pygame.Rect(self.current_coords[0] - self.bird_radius, self.current_coords[1] - self.bird_radius, self.bird_radius * 2, self.bird_radius * 2)

        # Buttons
        self.resetButton = Button(self.screen, x=0, y=0, width=80, height=40, text="Restart", color=(125,125,125), hover_color=(255,255,255), text_color=(0,0,0))
        
        # Sounds
        self.launch_sound = pygame.mixer.Sound("cleanerSlingshot/launch.mp3")
        self.hit_sound = pygame.mixer.Sound("cleanerSlingshot/hit.mp3")

    def velocity_finder(self, x):
        return self.elastic_constant * x

    def xcord(self, u, s, t):
        return self.original_coords[0] + (u * np.cos(s) / self.c) * (1 - np.exp(-self.c * t))

    def ycord(self, u, s, t):
        term1 = u * np.sin(s) + self.g / self.c
        term2 = (u * np.sin(s) + self.g / self.c) * np.exp(-self.c * t)
        return self.original_coords[1] - ((term1 - term2) / self.c) - self.g * t / self.c

    def vx(self, u, s, t):
        return u * np.cos(s) * np.exp(-self.c * t)

    def vy(self, u, s, t):
        return (((u * np.sin(s) *self.c)+self.g)* np.exp(-self.c * t) - self.g)/self.c


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_coords[0] - self.bird_radius <= pygame.mouse.get_pos()[0] <= self.current_coords[0] + self.bird_radius and self.current_coords[1] - self.bird_radius <= pygame.mouse.get_pos()[1] <= self.current_coords[1] + self.bird_radius:
                self.bird_held = True
            elif self.resetButton.resetButtonCords(pygame.mouse.get_pos()):
                self.bird_held = False
                self.bird_flying = False
                self.current_coords = np.array([111, 323])
                self.original_coords = np.array([111, 323])
                self.u = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.bird_held:
                self.bird_held = False
                self.bird_flying = True
                self.start_time = pygame.time.get_ticks() / 1000
                self.u = self.velocity_finder(np.linalg.norm(self.original_coords - self.current_coords))
                self.angle = -np.arctan2(self.original_coords[1] - self.current_coords[1], self.original_coords[0] - self.current_coords[0])
                self.launch_sound.play()

    def update(self):
        if self.bird_held:
            self.current_coords[0], self.current_coords[1] = pygame.mouse.get_pos()
            self.angle = -np.arctan2(self.original_coords[1] - self.current_coords[1], self.original_coords[0] - self.current_coords[0])
            self.u = self.velocity_finder(np.linalg.norm(self.original_coords - self.current_coords))

        if self.bird_flying:
            current_time = pygame.time.get_ticks() / 1000
            t = (current_time - self.start_time) * self.time_factor
            self.current_coords[0] = self.xcord(self.u, self.angle, t)
            self.current_coords[1] = self.ycord(self.u, self.angle, t)

            if self.current_coords[0] + self.bird_radius >= self.background.x or self.current_coords[1] + self.bird_radius >= self.background.grassY:
                self.handle_collision(wall=self.current_coords[0] + self.bird_radius >= self.background.x)
                self.start_time = current_time
            
            for obstacle in self.background.obstacles:
                if obstacle.rect.collidepoint(self.current_coords) :
                    if obstacle.is_hit():
                        self.hit_sound.play()
                        self.background.obstacles.remove(obstacle)
                    #self.obstacle_collision(obstacle)
                    #self.start_time = current_time
            for obstacle in self.background.piglins:
                if obstacle.rect.collidepoint(self.current_coords) :
                    if obstacle.is_hit():
                        self.hit_sound.play()
                        self.background.piglins.remove(obstacle)
    #def obstacle_collision(self, obstacle):
    #    Background.obstacles.remove(obstacle)
    #    self.hit_sound.play()

    def handle_collision(self, wall):
        t = ((pygame.time.get_ticks() / 1000) - self.start_time) * self.time_factor
        if wall:
            new_vx = -self.vx(self.u, self.angle, t)
            new_vy = self.vy(self.u, self.angle, t)
            self.u = self.elasticity * np.linalg.norm([new_vx, new_vy])
            self.angle = np.arctan2(new_vy, new_vx)
            self.original_coords = [self.background.x - self.bird_radius, self.current_coords[1]]
            self.current_coords[0] = self.original_coords[0]
        else:
            new_vx = self.vx(self.u, self.angle, t)
            new_vy = -self.vy(self.u, self.angle, t)
            self.u = self.elasticity * np.linalg.norm([new_vy, new_vx])
            self.angle = np.arctan2(new_vy, new_vx)
            self.current_coords[1] = self.background.grassY - self.bird_radius - 1
            self.original_coords[1] = self.current_coords[1]
            self.original_coords[0] = self.current_coords[0]

        # Stop the bird if the velocity is too low
        if self.u < self.min_velocity_threshold:
            self.bird_flying = False
            self.bird_held = False
            self.u = 0

        self.start_time = pygame.time.get_ticks() / 1000
        self.hit_sound.play()

    def draw_projection(self):
        if self.bird_held:
            points = []
            for i in range(1, 101):
                t = i * 0.1  # Incremental time for projection
                x = self.xcord(self.u, self.angle, t)
                y = self.ycord(self.u, self.angle, t)
                if x > self.background.x or y > 600:
                    break
                points.append((int(x), int(y)))
            if len(points) > 1:
                pygame.draw.lines(self.screen, (0, 0, 0), False, points, 1)

    #def draw(self):
    #    self.draw_projection()
    #    pygame.draw.circle(self.screen, (255, 0, 0), (int(self.current_coords[0]), int(self.current_coords[1])), self.bird_radius)
    #    self.resetButton.draw()

    def draw(self):
        self.draw_projection()

        bird_image = pygame.Surface((self.bird_radius * 2, self.bird_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bird_image, (255, 0, 0), (self.bird_radius, self.bird_radius), self.bird_radius)
        
        # Draw eyes
        eye_radius = 3
        eye_x_offset = 5
        eye_y_offset = 5
        pygame.draw.circle(bird_image, (255, 255, 255), (self.bird_radius - eye_x_offset, self.bird_radius - eye_y_offset), eye_radius)
        pygame.draw.circle(bird_image, (255, 255, 255), (self.bird_radius + eye_x_offset, self.bird_radius - eye_y_offset), eye_radius)
        pygame.draw.circle(bird_image, (0, 0, 0), (self.bird_radius - eye_x_offset, self.bird_radius - eye_y_offset), 1)
        pygame.draw.circle(bird_image, (0, 0, 0), (self.bird_radius + eye_x_offset, self.bird_radius - eye_y_offset), 1)
        
        # Draw mouth
        mouth_start = (self.bird_radius - 5, self.bird_radius + 5)
        mouth_end = (self.bird_radius + 5, self.bird_radius + 5)
        pygame.draw.line(bird_image, (0, 0, 0), mouth_start, mouth_end, 2)
        
        if self.bird_flying:
            bird_image = pygame.transform.rotate(bird_image, -np.degrees(self.angle))
        
        rect = bird_image.get_rect(center=(int(self.current_coords[0]), int(self.current_coords[1])))
        self.screen.blit(bird_image, rect.topleft)
        self.resetButton.draw()
        
    def reset(self):
        self.resetButton.draw()
