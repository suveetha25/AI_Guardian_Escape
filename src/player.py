"""
=========================================
AI Guardian Escape
player.py

Player Class
=========================================
"""

import pygame

from settings import *


class Player:
    def __init__(self):
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

        self.rect = pygame.Rect(
            60,
            HEIGHT // 2,
            self.width,
            self.height
        )

        self.color = PLAYER_COLOR

        self.walk_speed = PLAYER_SPEED
        self.run_speed = PLAYER_RUN_SPEED
        self.speed = self.walk_speed

        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.inventory = []

        self.is_running = False
        self.is_invisible = False
        self.has_shield = False

        self.invisible_timer = 0
        self.speed_timer = 0

    # =========================================
    # Reset Player
    # =========================================
    def reset(self):
        self.rect.x = 60
        self.rect.y = HEIGHT // 2

        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.inventory.clear()

        self.is_running = False
        self.is_invisible = False
        self.has_shield = False

        self.invisible_timer = 0
        self.speed_timer = 0
        self.speed = self.walk_speed

    # =========================================
    # Movement
    # =========================================
    def move(self, walls):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        self.is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if self.speed_timer > 0:
            self.speed = self.run_speed + 2
        elif self.is_running:
            self.speed = self.run_speed
        else:
            self.speed = self.walk_speed

        if keys[pygame.K_w]:
            dy -= self.speed

        if keys[pygame.K_s]:
            dy += self.speed

        if keys[pygame.K_a]:
            dx -= self.speed

        if keys[pygame.K_d]:
            dx += self.speed

        self.rect.x += dx

        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    # =========================================
    # Update Timers
    # =========================================
    def update(self):
        if self.invisible_timer > 0:
            self.invisible_timer -= 1
            self.is_invisible = True
        else:
            self.is_invisible = False

        if self.speed_timer > 0:
            self.speed_timer -= 1
            self.speed = self.run_speed + 2
        else:
            if not self.is_running:
                self.speed = self.walk_speed

    # =========================================
    # Powerups
    # =========================================
    def activate_speed(self):
        self.speed_timer = FPS * POWERUP_DURATION

    def activate_invisibility(self):
        self.invisible_timer = FPS * INVISIBILITY_TIME

    def activate_shield(self):
        self.has_shield = True

    # =========================================
    # Damage
    # =========================================
    def take_damage(self):
        if self.has_shield:
            self.has_shield = False
            return

        self.health -= 1

    # =========================================
    # Healing
    # =========================================
    def heal(self):
        if self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    # =========================================
    # Score
    # =========================================
    def add_score(self, points):
        self.score += points

    # =========================================
    # Draw
    # =========================================
    def draw(self, screen):
        colour = self.color

        if self.is_invisible:
            colour = CYAN

        pygame.draw.rect(
            screen,
            colour,
            self.rect,
            border_radius=6
        )

        if self.has_shield:
            pygame.draw.circle(
                screen,
                YELLOW,
                self.rect.center,
                PLAYER_SIZE,
                2
            )