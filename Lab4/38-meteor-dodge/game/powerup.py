import math
import random

import pygame


class ShieldOrb:
    RADIUS = 11

    def __init__(self, width, height):
        self.x = random.randint(30, width - 30)
        self.y = random.randint(70, height - 150)
        self.vx = random.choice((-1, 1)) * random.uniform(0.6, 1.3)
        self.vy = random.uniform(0.25, 0.8)
        self.phase = random.uniform(0, math.tau)

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        self.phase += 0.08
        if self.x < self.RADIUS or self.x > width - self.RADIUS:
            self.vx *= -1
        if self.y < 45 or self.y > height - 45:
            self.vy *= -1

    def collides(self, rect):
        dx = self.x - rect.centerx
        dy = self.y - rect.centery
        return math.hypot(dx, dy) < self.RADIUS + 20

    def draw(self, screen):
        pulse = int(3 + 2 * (1 + math.sin(self.phase)) / 2)
        pygame.draw.circle(screen, (70, 210, 255), (int(self.x), int(self.y)), self.RADIUS + pulse, 2)
        pygame.draw.circle(screen, (120, 235, 255), (int(self.x), int(self.y)), self.RADIUS - 2)
        pygame.draw.circle(screen, (220, 255, 255), (int(self.x), int(self.y)), 4)
