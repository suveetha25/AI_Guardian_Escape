"""
=========================================
AI Guardian Escape
effects.py

Visual Effects
-----------------------------------------
• Screen Fade
• Portal Glow
• Magic Aura
• Flash Effect
=========================================
"""

import pygame

from settings import *


class FadeEffect:
    def __init__(self):
        self.alpha = 255
        self.speed = 6
        self.active = False
        self.fade_in = True

    # ----------------------------------
    def start_fade_in(self):
        self.alpha = 255
        self.fade_in = True
        self.active = True

    # ----------------------------------
    def start_fade_out(self):
        self.alpha = 0
        self.fade_in = False
        self.active = True

    # ----------------------------------
    def update(self):
        if not self.active:
            return

        if self.fade_in:
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
        else:
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False

    # ----------------------------------
    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(self.alpha)
        screen.blit(overlay, (0, 0))


class PortalGlow:
    def __init__(self):
        self.radius = 40
        self.direction = 1

    def update(self):
        self.radius += self.direction

        if self.radius >= 55:
            self.direction = -1

        if self.radius <= 40:
            self.direction = 1

    def draw(self, screen, portal):
        pygame.draw.circle(
            screen,
            CYAN,
            portal.center,
            self.radius,
            3
        )


class MagicAura:
    def __init__(self):
        self.radius = 22
        self.direction = 1

    def update(self):
        self.radius += self.direction

        if self.radius >= 28:
            self.direction = -1

        if self.radius <= 22:
            self.direction = 1

    def draw(self, screen, player):
        pygame.draw.circle(
            screen,
            PURPLE,
            player.rect.center,
            self.radius,
            2
        )


class FlashEffect:
    def __init__(self):
        self.alpha = 0

    def trigger(self):
        self.alpha = 180

    def update(self):
        if self.alpha > 0:
            self.alpha -= 8

        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        if self.alpha <= 0:
            return

        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.fill(WHITE)
        flash.set_alpha(self.alpha)
        screen.blit(flash, (0, 0))