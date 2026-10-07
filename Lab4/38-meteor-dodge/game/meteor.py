import pygame
import random
import math


class Meteor:
    def __init__(self, width, x=None, y=-30, radius=None):
        self.x = random.randint(0, width) if x is None else x
        self.y = y
        self.radius = random.randint(12, 28) if radius is None else radius

        angle = random.uniform(70, 110)
        speed = random.uniform(2, 5)

        self.vx = math.cos(math.radians(angle)) * speed
        self.vy = math.sin(math.radians(angle)) * speed

        self.color = (
            random.randint(160, 220),
            random.randint(80, 120),
            random.randint(40, 80)
        )

        self.rot = 0
        self.rot_speed = random.uniform(-3, 3)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery

        dx = self.x - cx
        dy = self.y - cy

        return (dx ** 2 + dy ** 2) ** 0.5 < self.radius + 16

    def split(self):
        if self.radius <= 14:
            return []

        new_radius = self.radius // 2

        return [
            Meteor(
                700,
                self.x - new_radius,
                self.y,
                new_radius
            ),
            Meteor(
                700,
                self.x + new_radius,
                self.y,
                new_radius
            )
        ]

    def draw(self, screen):
        points = []

        for i in range(7):
            angle = math.radians(
                self.rot + i * (360 / 7)
            )

            radius = self.radius * (
                0.8 + 0.2 * (i % 2)
            )

            points.append(
                (
                    int(
                        self.x
                        + radius * math.cos(angle)
                    ),
                    int(
                        self.y
                        + radius * math.sin(angle)
                    )
                )
            )

        pygame.draw.polygon(
            screen,
            self.color,
            points
        )

        inner = [
            (
                int(
                    self.x
                    + (self.radius * 0.5)
                    * math.cos(
                        math.radians(
                            self.rot + i * (360 / 7)
                        )
                    )
                ),
                int(
                    self.y
                    + (self.radius * 0.5)
                    * math.sin(
                        math.radians(
                            self.rot + i * (360 / 7)
                        )
                    )
                )
            )
            for i in range(7)
        ]

        pygame.draw.polygon(
            screen,
            tuple(
                max(0, c - 40)
                for c in self.color
            ),
            inner
        )