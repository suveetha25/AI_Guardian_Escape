"""
=========================================
AI Guardian Escape
map.py

Adventure Map

Supports
• Level Unlocking
=========================================
"""

import pygame

from settings import *


class AdventureMap:
    def __init__(self):
        self.levels = [
            {
                "id": FOREST,
                "name": "Forest",
                "position": (180, 360)
            },
            {
                "id": CASTLE,
                "name": "Castle",
                "position": (430, 240)
            },
            {
                "id": SNOW,
                "name": "Snow",
                "position": (720, 360)
            },
            {
                "id": VOLCANO,
                "name": "Volcano",
                "position": (1050, 250)
            }
        ]

        self.selected = 0

        self.unlocked = {
            FOREST: True,
            CASTLE: False,
            SNOW: False,
            VOLCANO: False
        }

        self.title_font = pygame.font.SysFont("arial", 50, bold=True)
        self.font = pygame.font.SysFont("arial", 28)

    # ===================================
    # Unlock Next Level
    # ===================================
    def unlock(self, level):
        self.unlocked[level] = True

    # ===================================
    # Navigation
    # ===================================
    def move_left(self):
        if self.selected > 0:
            self.selected -= 1

    def move_right(self):
        if self.selected < len(self.levels) - 1:
            self.selected += 1

    def reset_selection(self):
        self.selected = 0

    # ===================================
    # Current Level
    # ===================================
    def get_level(self):
        return self.levels[self.selected]["id"]

    def can_play(self):
        return self.unlocked[self.get_level()]

    # ===================================
    # Draw
    # ===================================
    def draw(self, screen):
        screen.fill((30, 35, 60))

        title = self.title_font.render(
            "Adventure Map",
            True,
            YELLOW
        )
        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                40
            )
        )

        for i in range(len(self.levels) - 1):
            pygame.draw.line(
                screen,
                LIGHT_GREY,
                self.levels[i]["position"],
                self.levels[i + 1]["position"],
                4
            )

        for index, level in enumerate(self.levels):
            if self.unlocked[level["id"]]:
                colour = GREEN
            else:
                colour = GREY

            if index == self.selected:
                colour = CYAN

            pygame.draw.circle(
                screen,
                colour,
                level["position"],
                35
            )

            label = self.font.render(
                level["name"],
                True,
                WHITE
            )
            screen.blit(
                label,
                (
                    level["position"][0] - label.get_width() // 2,
                    level["position"][1] + 55
                )
            )

            if not self.unlocked[level["id"]]:
                lock = self.font.render(
                    "Locked",
                    True,
                    RED
                )
                screen.blit(
                    lock,
                    (
                        level["position"][0] - lock.get_width() // 2,
                        level["position"][1] - 70
                    )
                )

        controls = self.font.render(
            "← → Select ENTER Play ESC Menu",
            True,
            WHITE
        )
        screen.blit(
            controls,
            (
                WIDTH // 2 - controls.get_width() // 2,
                HEIGHT - 60
            )
        )