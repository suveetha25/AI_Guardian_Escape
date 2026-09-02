"""
=========================================
AI Guardian Escape
menu.py

Main Menu System
=========================================
"""

import math
import pygame

from settings import *


class Menu:
    def __init__(self):
        self.options = [
            "Play",
            "Adventure Map",
            "How To Play",
            "Settings",
            "Exit"
        ]

        self.selected = 0

        self.title_font = pygame.font.SysFont("arial", 58, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 28)
        self.option_font = pygame.font.SysFont("arial", 34, bold=True)
        self.small_font = pygame.font.SysFont("arial", 22)

        self.anim_time = 0

    # =====================================
    # Move Selection
    # =====================================
    def move_up(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.options) - 1

    def move_down(self):
        self.selected += 1
        if self.selected >= len(self.options):
            self.selected = 0

    # =====================================
    # Get Current Option
    # =====================================
    def get_selected(self):
        return self.options[self.selected]

    # =====================================
    # Background
    # =====================================
    def _draw_background(self, screen, colour1=(24, 24, 44), colour2=(44, 34, 78)):
        self.anim_time += 0.02
        screen.fill(colour1)

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for x, y, r, c in [
            (220, 130, 160, (100, 180, 255, 28)),
            (1000, 160, 190, (255, 120, 210, 24)),
            (640, 580, 220, (255, 220, 110, 20)),
        ]:
            pygame.draw.circle(glow, c, (x, y), r)

        screen.blit(glow, (0, 0))

        for i in range(12):
            px = 80 + i * 95
            py = 80 + int(math.sin(self.anim_time + i * 0.5) * 8)
            pygame.draw.circle(screen, (255, 255, 255), (px, py), 2)

        for i in range(10):
            px = 100 + i * 110
            py = HEIGHT - 70 + int(math.cos(self.anim_time + i * 0.45) * 6)
            pygame.draw.circle(screen, (255, 235, 180), (px, py), 2)

    def _draw_panel(self, screen, rect, fill=(18, 16, 32, 185), border=WHITE):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel.fill(fill)
        screen.blit(panel, rect.topleft)
        pygame.draw.rect(screen, border, rect, 2, border_radius=18)

    # =====================================
    # Draw Menu
    # =====================================
    def draw(self, screen):
        self._draw_background(screen)

        title = self.title_font.render("AI GUARDIAN ESCAPE", True, YELLOW)
        subtitle = self.subtitle_font.render("The Magical Worlds", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 74))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 145))

        menu_box = pygame.Rect(WIDTH // 2 - 210, 235, 420, 340)
        self._draw_panel(screen, menu_box, fill=(18, 18, 34, 185), border=(220, 230, 255))

        start_y = menu_box.y + 42

        for index, option in enumerate(self.options):
            selected = index == self.selected

            if selected:
                glow_rect = pygame.Rect(menu_box.x + 28, start_y - 6 + index * 56, menu_box.width - 56, 42)
                pygame.draw.rect(screen, (70, 95, 165), glow_rect, border_radius=12)
                pygame.draw.rect(screen, CYAN, glow_rect, 2, border_radius=12)

            colour = YELLOW if selected else WHITE
            prefix = "✦ " if selected else "  "
            text = self.option_font.render(prefix + option, True, colour)

            screen.blit(
                text,
                (menu_box.x + 54, start_y + index * 56)
            )

        controls = self.small_font.render("↑ ↓ Navigate    ENTER Select", True, LIGHT_GREY)
        screen.blit(
            controls,
            (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 58)
        )

    # =====================================
    # How To Play Screen
    # =====================================
    def draw_help(self, screen):
        self._draw_background(screen, colour1=(16, 18, 28), colour2=(40, 40, 65))

        title = self.title_font.render("HOW TO PLAY", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 54))

        panel = pygame.Rect(120, 150, WIDTH - 240, 450)
        self._draw_panel(screen, panel, fill=(20, 20, 35, 195), border=(225, 235, 255))

        lines = [
            "W A S D  : Move through the magical world",
            "SHIFT    : Run faster",
            "E        : Collect the nearby magical object",
            "ESC      : Pause or return",
            "",
            "Goal:",
            "Collect enough magical objects to unlock the portal.",
            "Avoid the AI Guardian while exploring each level.",
            "Reach the glowing portal to escape safely.",
            "",
            "Press ESC to return."
        ]

        y = panel.y + 36
        for i, line in enumerate(lines):
            if line == "Goal:":
                colour = CYAN
                font = self.option_font
            else:
                colour = WHITE
                font = self.subtitle_font

            image = font.render(line, True, colour)
            screen.blit(image, (panel.x + 40, y))
            y += 38

    # =====================================
    # Settings Screen
    # =====================================
    def draw_settings(self, screen):
        self._draw_background(screen, colour1=(22, 20, 38), colour2=(48, 28, 60))

        title = self.title_font.render("SETTINGS", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

        panel = pygame.Rect(WIDTH // 2 - 280, 170, 560, 360)
        self._draw_panel(screen, panel, fill=(22, 18, 38, 195), border=(230, 220, 255))

        lines = [
            "Resolution   : 1280 x 720",
            "Frame Rate   : 60 FPS",
            "AI Behaviour : FSM Based",
            "Graphics     : Cute Drawn Fantasy Style",
            "",
            "Press ESC to return"
        ]

        y = panel.y + 48
        for line in lines:
            colour = WHITE if "Press ESC" not in line else CYAN
            image = self.subtitle_font.render(line, True, colour)
            screen.blit(image, (panel.x + 50, y))
            y += 42