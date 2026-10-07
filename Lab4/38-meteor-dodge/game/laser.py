import pygame


class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 3, y - 16, 6, 16)
        self.speed = 10
        self.color = (100, 255, 120)

    def update(self):
        self.rect.y -= self.speed

    def off_screen(self):
        return self.rect.bottom < 0

    def collides(self, meteor):
        dx = meteor.x - self.rect.centerx
        dy = meteor.y - self.rect.centery

        distance = (dx ** 2 + dy ** 2) ** 0.5

        return distance < meteor.radius + 4

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect
        )