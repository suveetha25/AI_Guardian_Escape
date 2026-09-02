"""
=========================================
AI Guardian Escape
level.py

Handles

• Level Loading
• Walls
• Collectibles
• Portal
• Timer
• Star Rating
=========================================
"""

import math
import pygame

from settings import *
from levels import LEVELS
from collectibles import create_collectibles


class Level:
    def __init__(self, level_number):
        self.load(level_number)

    # =====================================
    # Load Level
    # =====================================
    def load(self, level_number):
        self.level_number = level_number
        data = LEVELS[level_number]

        self.name = data["name"]
        self.background = data["background"]
        self.guardian_name = data["guardian_name"]
        self.difficulty = data["difficulty"]
        self.portal = data["portal"].copy()
        self.walls = data["walls"]
        self.collectible_type = data["collectible_type"]

        self.collectibles = create_collectibles(
            level_number,
            self.walls,
            self.portal
        )

        self.total_collectibles = len(self.collectibles)
        self.collected = 0
        self.timer = LEVEL_TIME[level_number] * FPS
        self.portal_open = False
        self.anim_time = 0

        if level_number == FOREST:
            self.required_collectibles = 3
        elif level_number == CASTLE:
            self.required_collectibles = 3
        elif level_number == SNOW:
            self.required_collectibles = 2
        else:
            self.required_collectibles = 2

        self.play_area = pygame.Rect(34, 34, WIDTH - 68, HEIGHT - 68)
        self.inner_area = self.play_area.inflate(-18, -18)

    # =====================================
    # Update
    # =====================================
    def update(self, player):
        self.anim_time += 0.03

        if self.timer > 0:
            self.timer -= 1

        for collectible in self.collectibles:
            collectible.update()

            if collectible.collect(player):
                self.collected += 1

        if self.collected >= self.required_collectibles:
            self.portal_open = True

    # =====================================
    # Timer
    # =====================================
    def time_up(self):
        return self.timer <= 0

    # =====================================
    # Portal
    # =====================================
    def reached_portal(self, player):
        if not self.portal_open:
            return False

        return player.rect.colliderect(self.portal)

    # =====================================
    # Level Complete
    # =====================================
    def is_complete(self):
        return self.portal_open

    # =====================================
    # Mission Progress
    # =====================================
    def mission_progress(self):
        return f"{self.collected}/{self.total_collectibles}"

    # =====================================
    # Star Rating
    # =====================================
    def get_stars(self):
        if self.level_number == FOREST:
            if self.collected >= 6:
                return 3
            elif self.collected >= 5:
                return 2
            elif self.collected >= 3:
                return 1

        elif self.level_number == CASTLE:
            if self.collected >= 5:
                return 3
            elif self.collected >= 4:
                return 2
            elif self.collected >= 3:
                return 1

        elif self.level_number == SNOW:
            if self.collected >= 4:
                return 3
            elif self.collected >= 3:
                return 2
            elif self.collected >= 2:
                return 1

        elif self.level_number == VOLCANO:
            if self.collected >= 3:
                return 3
            elif self.collected >= 2:
                return 2

        return 0

    # =====================================
    # Theme Helpers
    # =====================================
    def _theme_colours(self):
        if self.level_number == FOREST:
            return {
                "border": (36, 84, 40),
                "inner": (210, 245, 205),
                "wall_main": (103, 84, 57),
                "wall_shadow": (65, 49, 30),
                "wall_highlight": (145, 118, 82),
                "portal": (110, 220, 255),
                "portal_ring": (215, 250, 255),
                "spark": (160, 255, 180)
            }
        if self.level_number == CASTLE:
            return {
                "border": (78, 72, 100),
                "inner": (232, 228, 246),
                "wall_main": (123, 123, 145),
                "wall_shadow": (84, 84, 103),
                "wall_highlight": (165, 165, 188),
                "portal": (180, 120, 255),
                "portal_ring": (240, 225, 255),
                "spark": (220, 200, 255)
            }
        if self.level_number == SNOW:
            return {
                "border": (110, 145, 170),
                "inner": (255, 255, 255),
                "wall_main": (210, 230, 245),
                "wall_shadow": (160, 190, 220),
                "wall_highlight": (255, 255, 255),
                "portal": (120, 245, 255),
                "portal_ring": (240, 255, 255),
                "spark": (255, 255, 255)
            }
        return {
            "border": (105, 42, 20),
            "inner": (255, 222, 190),
            "wall_main": (140, 62, 34),
            "wall_shadow": (88, 30, 12),
            "wall_highlight": (182, 98, 60),
            "portal": (255, 145, 55),
            "portal_ring": (255, 230, 170),
            "spark": (255, 190, 120)
        }

    def _draw_background_decor(self, screen, colours):
        for i in range(8):
            x = 90 + i * 145
            y = 62
            pygame.draw.circle(screen, colours["inner"], (x, y), 3)

        for i in range(6):
            x = 70 + i * 210
            y = HEIGHT - 58
            pygame.draw.circle(screen, colours["inner"], (x, y), 3)

    def _draw_wall(self, screen, wall, colours):
        shadow = wall.move(4, 4)
        pygame.draw.rect(screen, colours["wall_shadow"], shadow, border_radius=10)
        pygame.draw.rect(screen, colours["wall_main"], wall, border_radius=10)
        pygame.draw.rect(screen, colours["wall_highlight"], wall, 2, border_radius=10)

        top_strip = pygame.Rect(wall.x + 4, wall.y + 4, max(8, wall.width - 8), 5)
        if top_strip.width > 0 and top_strip.height > 0:
            pygame.draw.rect(screen, colours["inner"], top_strip, border_radius=3)

    def _draw_portal(self, screen, colours):
        portal_center = self.portal.center
        glow_surface = pygame.Surface((160, 160), pygame.SRCALPHA)

        pulse = 6 * math.sin(self.anim_time * 3.2)
        base_radius = 28 + pulse

        for radius, alpha in [(54, 20), (42, 35), (32, 55)]:
            pygame.draw.circle(
                glow_surface,
                (*colours["portal"], alpha),
                (80, 80),
                int(radius + pulse)
            )

        screen.blit(
            glow_surface,
            (portal_center[0] - 80, portal_center[1] - 80)
        )

        outer = self.portal.inflate(18, 12)
        pygame.draw.ellipse(screen, colours["portal_ring"], outer, 4)
        pygame.draw.ellipse(screen, colours["portal"], self.portal, 0)

        inner = self.portal.inflate(-16, -14)
        pygame.draw.ellipse(screen, colours["portal_ring"], inner, 2)

        swirl_rect = inner.inflate(-8, -10)
        if swirl_rect.width > 6 and swirl_rect.height > 6:
            pygame.draw.arc(
                screen,
                WHITE,
                swirl_rect,
                0.5 + self.anim_time,
                3.8 + self.anim_time,
                3
            )
            pygame.draw.arc(
                screen,
                colours["spark"],
                swirl_rect.inflate(-10, -10),
                3.5 - self.anim_time,
                6.0 - self.anim_time,
                2
            )

        if not self.portal_open:
            lock_bar = pygame.Rect(
                self.portal.centerx - 10,
                self.portal.centery - 16,
                20,
                32
            )
            pygame.draw.rect(screen, RED, lock_bar, border_radius=6)
            pygame.draw.rect(screen, WHITE, lock_bar, 2, border_radius=6)

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        colours = self._theme_colours()

        screen.fill(self.background)

        frame_shadow = self.play_area.move(6, 6)
        pygame.draw.rect(screen, (0, 0, 0), frame_shadow, border_radius=18)
        pygame.draw.rect(screen, colours["border"], self.play_area, border_radius=18)
        pygame.draw.rect(screen, colours["inner"], self.inner_area, 3, border_radius=14)

        self._draw_background_decor(screen, colours)

        for wall in self.walls:
            self._draw_wall(screen, wall, colours)

        for collectible in self.collectibles:
            collectible.draw(screen)

        self._draw_portal(screen, colours)

    # =====================================
    # HUD Timer
    # =====================================
    def get_timer(self):
        seconds = self.timer // FPS
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"