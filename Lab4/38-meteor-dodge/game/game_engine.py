import pygame

from game.meteor import Meteor
from game.ship import Ship
from game.powerup import ShieldOrb


WIDTH = 700
HEIGHT = 700
FPS = 60


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meteor Dodge")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 64)

        self.ship = Ship(WIDTH // 2, HEIGHT - 80)

        self.meteors = []
        self.lasers = []
        self.shield_orbs = []

        self.score = 0
        self.game_over = False
        self.started = False

        self.spawn_timer = 0
        self.powerup_timer = 0

        self.shield_active = False

        # Survival multiplier
        self.survival_frames = 0

    def reset(self):
        self.ship = Ship(WIDTH // 2, HEIGHT - 80)

        self.meteors.clear()
        self.lasers.clear()
        self.shield_orbs.clear()

        self.score = 0
        self.game_over = False
        self.started = False

        self.spawn_timer = 0
        self.powerup_timer = 0

        self.shield_active = False

        # Reset survival streak
        self.survival_frames = 0

    def spawn_meteor(self):
        self.meteors.append(Meteor(WIDTH))

    def spawn_shield(self):
        self.shield_orbs.append(
            ShieldOrb(WIDTH, HEIGHT)
        )

    def update(self):
        if not self.started or self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.ship.move(keys, WIDTH, HEIGHT)

        # Count uninterrupted survival time
        self.survival_frames += 1

        # Spawn meteors
        self.spawn_timer += 1

        if self.spawn_timer >= 35:
            self.spawn_timer = 0
            self.spawn_meteor()

        # Spawn shield orb periodically
        self.powerup_timer += 1

        if self.powerup_timer >= 600:
            self.powerup_timer = 0

            if not self.shield_active and not self.shield_orbs:
                self.spawn_shield()

        # Update meteors
        for meteor in self.meteors:
            meteor.update()

        # Update lasers
        for laser in self.lasers:
            laser.update()

        # Update shield orbs
        for orb in self.shield_orbs:
            orb.update(WIDTH, HEIGHT)

        # Remove objects outside screen
        self.meteors = [
            meteor
            for meteor in self.meteors
            if not meteor.off_screen(HEIGHT)
        ]

        self.lasers = [
            laser
            for laser in self.lasers
            if not laser.off_screen(HEIGHT)
        ]

        # Collect shield orb
        remaining_orbs = []

        for orb in self.shield_orbs:
            if orb.collides(self.ship.rect):
                self.shield_active = True
            else:
                remaining_orbs.append(orb)

        self.shield_orbs = remaining_orbs

        # Laser / meteor collisions
        remaining_meteors = []
        used_lasers = set()

        for meteor in self.meteors:
            destroyed = False

            for index, laser in enumerate(self.lasers):
                if index in used_lasers:
                    continue

                if laser.collides(meteor):
                    destroyed = True
                    used_lasers.add(index)

                    # Score increases according to survival multiplier
                    multiplier = (
                        1
                        + self.survival_frames // (10 * FPS)
                    )

                    self.score += 100 * multiplier

                    fragments = meteor.split()
                    remaining_meteors.extend(fragments)

                    break

            if not destroyed:
                remaining_meteors.append(meteor)

        self.meteors = remaining_meteors

        self.lasers = [
            laser
            for index, laser in enumerate(self.lasers)
            if index not in used_lasers
        ]

        # Meteor / ship collisions
        for meteor in self.meteors:
            if meteor.collides(self.ship.rect):

                if self.shield_active:
                    # Shield absorbs the collision
                    self.shield_active = False

                    # Reset survival streak and multiplier
                    self.survival_frames = 0

                    # Remove the meteor that hit the shield
                    meteor.y = HEIGHT + 100

                    continue

                self.game_over = True
                break

    def draw(self):
        self.screen.fill((10, 10, 10))

        # Draw meteors
        for meteor in self.meteors:
            meteor.draw(self.screen)

        # Draw lasers
        for laser in self.lasers:
            laser.draw(self.screen)

        # Draw shield orbs
        for orb in self.shield_orbs:
            orb.draw(self.screen)

        # Draw ship
        self.ship.draw(self.screen)

        # Calculate current multiplier
        multiplier = (
            1
            + self.survival_frames // (10 * FPS)
        )

        # Score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(score_text, (15, 15))

        # Survival time
        time_text = self.font.render(
            f"Time: {self.survival_frames // FPS}s",
            True,
            (180, 220, 255)
        )

        self.screen.blit(time_text, (15, 50))

        # Multiplier
        multiplier_text = self.font.render(
            f"Multiplier: x{multiplier}",
            True,
            (255, 220, 80)
        )

        self.screen.blit(
            multiplier_text,
            (15, 85)
        )

        # Shield status
        if self.shield_active:
            shield_text = self.font.render(
                "SHIELD READY",
                True,
                (120, 235, 255)
            )

            self.screen.blit(
                shield_text,
                (15, 120)
            )

        # Start message
        if not self.started and not self.game_over:
            text = self.big_font.render(
                "PRESS SPACE TO START",
                True,
                (255, 255, 255)
            )

            rect = text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            self.screen.blit(text, rect)

        # Game over message
        if self.game_over:
            text = self.big_font.render(
                "GAME OVER",
                True,
                (255, 80, 80)
            )

            rect = text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 30)
            )

            self.screen.blit(text, rect)

            restart = self.font.render(
                "PRESS SPACE TO RESTART",
                True,
                (255, 255, 255)
            )

            restart_rect = restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 35)
            )

            self.screen.blit(
                restart,
                restart_rect
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:

                        if self.game_over:
                            self.reset()

                        elif not self.started:
                            self.started = True

                        else:
                            self.lasers.append(
                                self.ship.fire()
                            )

            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()