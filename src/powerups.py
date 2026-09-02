"""
=========================================
AI Guardian Escape
powerups.py

Powerup System
=========================================
"""

import random
import pygame

from settings import *


class PowerUp:
    def __init__(self, x, y, power_type):
        self.type = power_type

        self.rect = pygame.Rect(
            x,
            y,
            POWERUP_SIZE,
            POWERUP_SIZE
        )

        self.collected = False
        self.float_offset = 0
        self.float_direction = 1

        self.colours = {
            "speed": CYAN,
            "shield": YELLOW,
            "invisible": PURPLE,
            "health": GREEN
        }

        self.labels = {
            "speed": "S",
            "shield": "D",
            "invisible": "I",
            "health": "H"
        }

        self.font = pygame.font.SysFont("arial", 16, bold=True)

    # =====================================
    # Update
    # =====================================
    def update(self):
        self.float_offset += self.float_direction * 0.2

        if self.float_offset >= 4:
            self.float_direction = -1
        elif self.float_offset <= -4:
            self.float_direction = 1

    # =====================================
    # Collect
    # =====================================
    def collect(self, player):
        if self.collected:
            return False

        if not self.rect.colliderect(player.rect):
            return False

        self.collected = True

        if self.type == "speed":
            player.activate_speed()
        elif self.type == "shield":
            player.activate_shield()
        elif self.type == "invisible":
            player.activate_invisibility()
        elif self.type == "health":
            player.heal()

        player.add_score(50)
        return True

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        if self.collected:
            return

        draw_rect = self.rect.copy()
        draw_rect.y += int(self.float_offset)

        pygame.draw.rect(
            screen,
            self.colours[self.type],
            draw_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            WHITE,
            draw_rect,
            2,
            border_radius=8
        )

        label = self.font.render(self.labels[self.type], True, BLACK)
        screen.blit(
            label,
            (
                draw_rect.centerx - label.get_width() // 2,
                draw_rect.centery - label.get_height() // 2
            )
        )


class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.spawn_timer = FPS * 8
        self.max_powerups = 3

    # =====================================
    # Position Check
    # =====================================
    def _valid_spawn(self, rect):
        border = pygame.Rect(60, 60, WIDTH - 120, HEIGHT - 120)

        if not border.contains(rect):
            return False

        for powerup in self.powerups:
            if rect.colliderect(powerup.rect.inflate(30, 30)):
                return False

        return True

    # =====================================
    # Spawn Random PowerUp
    # =====================================
    def spawn_random(self):
        if len(self.powerups) >= self.max_powerups:
            return

        power_type = random.choice([
            "speed",
            "shield",
            "invisible",
            "health"
        ])

        for _ in range(100):
            x = random.randint(120, WIDTH - 120)
            y = random.randint(120, HEIGHT - 120)

            rect = pygame.Rect(x, y, POWERUP_SIZE, POWERUP_SIZE)
            if self._valid_spawn(rect):
                self.powerups.append(
                    PowerUp(x, y, power_type)
                )
                return

    # =====================================
    # Update
    # =====================================
    def update(self, player):
        self.spawn_timer -= 1

        if self.spawn_timer <= 0:
            self.spawn_random()
            self.spawn_timer = FPS * 10

        for powerup in self.powerups:
            powerup.update()
            powerup.collect(player)

        self.powerups = [p for p in self.powerups if not p.collected]

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)

    # =====================================
    # HUD Helper
    # =====================================
    def active_names(self, player):
        active = []

        if player.is_running or player.speed_timer > 0:
            active.append("Speed")

        if player.is_invisible:
            active.append("Invisible")

        if player.has_shield:
            active.append("Shield")

        return active

    # =====================================
    # Reset
    # =====================================
    def reset(self):
        self.powerups.clear()
        self.spawn_timer = FPS * 8


# ==========================================
# Compatibility Function
# ==========================================
def create_powerups():
    return PowerUpManager()