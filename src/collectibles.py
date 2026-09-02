"""
=========================================
AI Guardian Escape
collectibles.py

All collectible items for every level.
=========================================
"""

import math
import random
import pygame

from settings import *


class Collectible:
    def __init__(self, x, y, item_type="flower"):
        self.item_type = item_type

        self.rect = pygame.Rect(
            x,
            y,
            COLLECTIBLE_SIZE,
            COLLECTIBLE_SIZE
        )

        self.collected = False
        self.animation = random.uniform(0, 10)
        self.score_value = 100

    # =========================================
    # Update Animation
    # =========================================
    def update(self):
        self.animation += 0.12

    # =========================================
    # Collect
    # =========================================
    def collect(self, player):
        if self.collected:
            return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_e] and self.rect.colliderect(player.rect):
            self.collected = True
            player.add_score(self.score_value)
            return True

        return False

    # =========================================
    # Draw Helpers
    # =========================================
    def _draw_flower(self, surf, center):
        x, y = center
        petal_color = (255, 130, 190)
        middle = (255, 225, 90)
        leaf = (70, 185, 90)

        for ox, oy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
            pygame.draw.circle(surf, petal_color, (x + ox, y + oy), 4)

        pygame.draw.circle(surf, middle, center, 4)
        pygame.draw.line(surf, leaf, (x, y + 4), (x, y + 11), 2)
        pygame.draw.ellipse(surf, leaf, (x - 7, y + 5, 6, 4))
        pygame.draw.ellipse(surf, leaf, (x + 1, y + 6, 6, 4))

    def _draw_crystal(self, surf, center):
        x, y = center
        points = [
            (x, y - 8),
            (x + 6, y - 2),
            (x + 3, y + 8),
            (x - 3, y + 8),
            (x - 6, y - 2)
        ]
        pygame.draw.polygon(surf, (110, 255, 255), points)
        pygame.draw.polygon(surf, WHITE, points, 2)
        pygame.draw.line(surf, (190, 255, 255), (x, y - 8), (x, y + 8), 1)

    def _draw_ice(self, surf, center):
        x, y = center
        points = [
            (x, y - 8),
            (x + 5, y - 3),
            (x + 8, y + 2),
            (x + 2, y + 8),
            (x - 5, y + 6),
            (x - 8, y)
        ]
        pygame.draw.polygon(surf, (230, 245, 255), points)
        pygame.draw.polygon(surf, (160, 220, 255), points, 2)
        pygame.draw.circle(surf, WHITE, (x - 2, y - 2), 2)

    def _draw_brick(self, surf, center):
        x, y = center
        points = [
            (x - 7, y + 5),
            (x - 3, y - 6),
            (x + 4, y - 8),
            (x + 8, y + 3),
            (x + 1, y + 8)
        ]
        pygame.draw.polygon(surf, (255, 130, 40), points)
        pygame.draw.polygon(surf, (120, 45, 10), points, 2)
        pygame.draw.circle(surf, (255, 220, 120), (x + 1, y - 1), 2)

    # =========================================
    # Draw
    # =========================================
    def draw(self, screen):
        if self.collected:
            return

        bob = int(math.sin(self.animation * 2.5) * 2)
        center = (self.rect.centerx, self.rect.centery + bob)

        surf = pygame.Surface((COLLECTIBLE_SIZE + 18, COLLECTIBLE_SIZE + 18), pygame.SRCALPHA)
        local_center = (surf.get_width() // 2, surf.get_height() // 2)

        glow_color = {
            "flower": (255, 150, 210, 50),
            "crystal": (130, 255, 255, 55),
            "ice": (220, 245, 255, 55),
            "brick": (255, 145, 90, 50)
        }.get(self.item_type, (255, 220, 120, 50))

        for radius in (12, 9):
            pygame.draw.circle(surf, glow_color, local_center, radius)

        if self.item_type == "flower":
            self._draw_flower(surf, local_center)
        elif self.item_type == "crystal":
            self._draw_crystal(surf, local_center)
        elif self.item_type == "ice":
            self._draw_ice(surf, local_center)
        elif self.item_type == "brick":
            self._draw_brick(surf, local_center)

        screen.blit(
            surf,
            (
                center[0] - surf.get_width() // 2,
                center[1] - surf.get_height() // 2
            )
        )

    # =========================================
    # Reset
    # =========================================
    def reset(self):
        self.collected = False


def _item_type_for_level(level):
    if level == FOREST:
        return "flower"
    if level == CASTLE:
        return "crystal"
    if level == SNOW:
        return "ice"
    return "brick"


def _random_collectible_rect():
    margin = 90
    return pygame.Rect(
        random.randint(margin, WIDTH - margin - COLLECTIBLE_SIZE),
        random.randint(margin, HEIGHT - margin - COLLECTIBLE_SIZE),
        COLLECTIBLE_SIZE,
        COLLECTIBLE_SIZE
    )


def _is_valid_position(rect, walls, portal, existing):
    padding = 18
    test_rect = rect.inflate(padding * 2, padding * 2)

    border_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
    if not border_rect.contains(rect):
        return False

    if portal and test_rect.colliderect(portal.inflate(40, 40)):
        return False

    for wall in walls:
        if test_rect.colliderect(wall):
            return False

    for item in existing:
        if test_rect.colliderect(item.rect.inflate(30, 30)):
            return False

    player_spawn = pygame.Rect(40, HEIGHT // 2 - 50, 120, 100)
    if test_rect.colliderect(player_spawn):
        return False

    guardian_side = pygame.Rect(WIDTH - 250, 80, 210, HEIGHT - 160)
    if test_rect.colliderect(guardian_side):
        return False

    return True


# =============================================
# Factory Function
# =============================================
def create_collectibles(level, walls=None, portal=None):
    if walls is None:
        walls = []

    collectibles = []
    item_type = _item_type_for_level(level)
    target_count = COLLECTIBLE_COUNTS[level]

    attempts = 0
    max_attempts = 2000

    while len(collectibles) < target_count and attempts < max_attempts:
        attempts += 1
        rect = _random_collectible_rect()

        if _is_valid_position(rect, walls, portal, collectibles):
            collectibles.append(
                Collectible(rect.x, rect.y, item_type)
            )

    if len(collectibles) < target_count:
        fallback_positions = [
            (120, 120), (240, 180), (360, 260), (520, 420),
            (700, 180), (860, 320), (980, 500), (1080, 180)
        ]

        for x, y in fallback_positions:
            if len(collectibles) >= target_count:
                break

            rect = pygame.Rect(x, y, COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)
            if _is_valid_position(rect, walls, portal, collectibles):
                collectibles.append(
                    Collectible(rect.x, rect.y, item_type)
                )

    return collectibles