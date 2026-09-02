"""
=========================================
AI Guardian Escape
ui.py

Heads-Up Display (HUD)

Displays:
• Health
• Score
• Timer
• Level
• Mission Progress
• Guardian State
• Active Powerups
• Debug Information
=========================================
"""

import pygame

from settings import *


class UI:
    def __init__(self):
        pygame.font.init()

        self.font = pygame.font.SysFont("arial", FONT_SIZE)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 30, bold=True)
        self.message_font = pygame.font.SysFont("arial", 42, bold=True)

    # =====================================
    # Helper Panel
    # =====================================
    def _panel(self, screen, rect, fill=(25, 22, 40, 180), border=WHITE):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel.fill(fill)
        screen.blit(panel, rect.topleft)
        pygame.draw.rect(screen, border, rect, 2, border_radius=14)

    # =====================================
    # Draw HUD
    # =====================================
    def draw(self, screen, player, guardian, level):
        panel = pygame.Rect(18, 18, 320, 250)
        self._panel(screen, panel, fill=(18, 18, 32, 175), border=(235, 235, 255))

        title = self.small_font.render("MAGICAL STATUS", True, YELLOW)
        screen.blit(title, (panel.x + 16, panel.y + 12))

        health = "❤ " * player.health
        guardian_colour = RED if guardian.state == CHASE else GREEN

        powerups = []
        if player.is_running or player.speed_timer > 0:
            powerups.append("Speed")
        if player.is_invisible:
            powerups.append("Invisible")
        if player.has_shield:
            powerups.append("Shield")

        power_text_value = ", ".join(powerups) if powerups else "None"

        rows = [
            ("Health", health, RED),
            ("Score", str(player.score), WHITE),
            ("Level", level.name, WHITE),
            ("Mission", level.mission_progress(), CYAN),
            ("Time", level.get_timer(), YELLOW),
            ("Guardian", guardian.state, guardian_colour),
            ("Powerups", power_text_value, GREEN),
        ]

        y = panel.y + 42
        for label, value, colour in rows:
            label_img = self.small_font.render(f"{label} :", True, LIGHT_GREY)
            value_img = self.small_font.render(value, True, colour)

            screen.blit(label_img, (panel.x + 16, y))
            screen.blit(value_img, (panel.x + 120, y))
            y += 28

    # =====================================
    # Debug Window
    # =====================================
    def draw_debug(self, screen, guardian, player):
        panel = pygame.Rect(WIDTH - 345, 16, 325, 240)
        self._panel(screen, panel, fill=(10, 10, 18, 190), border=CYAN)

        lines = [
            "DEBUG MODE",
            "",
            f"State : {guardian.state}",
            f"Visible : {guardian.player_visible}",
            f"Speed : {guardian.current_speed}",
            f"Detection : {guardian.detection_radius}",
            f"Search Timer : {guardian.search_timer}",
            f"Player : {player.rect.center}",
            f"Guardian : {guardian.rect.center}"
        ]

        y = panel.y + 14
        for i, line in enumerate(lines):
            colour = YELLOW if i == 0 else WHITE
            image = self.small_font.render(line, True, colour)
            screen.blit(image, (panel.x + 14, y))
            y += 23

    # =====================================
    # Center Message
    # =====================================
    def center_message(self, screen, message, colour=WHITE):
        box = pygame.Rect(WIDTH // 2 - 280, HEIGHT // 2 - 55, 560, 110)
        self._panel(screen, box, fill=(20, 16, 35, 190), border=colour)

        image = self.message_font.render(message, True, colour)
        screen.blit(
            image,
            (
                WIDTH // 2 - image.get_width() // 2,
                HEIGHT // 2 - image.get_height() // 2
            )
        )