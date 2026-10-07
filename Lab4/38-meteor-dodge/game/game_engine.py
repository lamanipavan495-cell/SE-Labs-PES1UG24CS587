import pygame
import random

from game.ship import Ship
from game.meteor import Meteor


WIDTH, HEIGHT = 700, 520
FPS = 60
BG = (8, 5, 20)


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meteor Dodge")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(
            "monospace",
            26,
            bold=True
        )
        self.big_font = pygame.font.SysFont(
            "monospace",
            46,
            bold=True
        )

        self.stars = [
            (
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(1, 3),
            )
            for _ in range(80)
        ]

        self.reset()

    def reset(self):
        self.ship = Ship(WIDTH // 2, HEIGHT - 80)
        self.meteors = []
        self.lasers = []

        self.timer = 0
        self.spawn_interval = 60
        self.score = 0

        self.game_over = False
        self.started = False

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    if self.game_over:
                        self.reset()
                        self.started = True

                    elif not self.started:
                        self.started = True

                    else:
                        self.lasers.append(
                            self.ship.fire()
                        )

        return True

    def update(self):
        if self.game_over or not self.started:
            return

        keys = pygame.key.get_pressed()

        self.ship.move(
            keys,
            WIDTH,
            HEIGHT
        )

        self.timer += 1

        if self.timer >= self.spawn_interval:
            self.meteors.append(
                Meteor(WIDTH)
            )

            self.timer = 0

            self.spawn_interval = max(
                20,
                self.spawn_interval - 0.3
            )

        for meteor in self.meteors:
            meteor.update()

            if meteor.collides(
                self.ship.rect
            ):
                self.game_over = True

        for laser in self.lasers:
            laser.update()

        self.lasers = [
            laser
            for laser in self.lasers
            if not laser.off_screen()
        ]

        remaining_meteors = []
        used_lasers = set()

        for meteor in self.meteors:

            destroyed = False

            for index, laser in enumerate(
                self.lasers
            ):

                if index in used_lasers:
                    continue

                if laser.collides(meteor):

                    destroyed = True
                    used_lasers.add(index)

                    self.score += 100

                    break

            if not destroyed and not meteor.off_screen(
                HEIGHT
            ):
                remaining_meteors.append(meteor)

        self.meteors = remaining_meteors

        self.lasers = [
            laser
            for index, laser in enumerate(
                self.lasers
            )
            if index not in used_lasers
        ]

        self.score += 1

    def draw(self):
        self.screen.fill(BG)

        for sx, sy, sr in self.stars:
            pygame.draw.circle(
                self.screen,
                (200, 200, 220),
                (sx, sy),
                sr
            )

        for meteor in self.meteors:
            meteor.draw(self.screen)

        for laser in self.lasers:
            laser.draw(self.screen)

        self.ship.draw(self.screen)

        score_text = self.font.render(
            f"Time: {self.score // 60}s",
            True,
            (200, 200, 240)
        )

        self.screen.blit(
            score_text,
            (10, 10)
        )

        if not self.started:

            message = self.font.render(
                "Press SPACE to launch",
                True,
                (180, 180, 240)
            )

            self.screen.blit(
                message,
                (
                    WIDTH // 2 - message.get_width() // 2,
                    HEIGHT // 2
                )
            )

        if self.game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 150)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = self.big_font.render(
                "DESTROYED!",
                True,
                (220, 80, 60)
            )

            restart_text = self.font.render(
                f"Survived {self.score // 60}s | SPACE to Restart",
                True,
                (200, 200, 200)
            )

            self.screen.blit(
                game_over_text,
                (
                    WIDTH // 2
                    - game_over_text.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )

            self.screen.blit(
                restart_text,
                (
                    WIDTH // 2
                    - restart_text.get_width() // 2,
                    HEIGHT // 2 + 20
                )
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()