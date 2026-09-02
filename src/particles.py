"""
=========================================
AI Guardian Escape
particles.py

Particle System

Supports:
• Sparkles
• Snow
• Fire
• Portal Glow
=========================================
"""

import random
import pygame

from settings import *


class Particle:
    def __init__(self, x, y, colour, size, life):
        self.x = float(x)
        self.y = float(y)

        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)

        self.size = size
        self.life = life
        self.colour = colour

    # =====================================
    # Update
    # =====================================
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        if self.life <= 0:
            return

        pygame.draw.circle(
            screen,
            self.colour,
            (int(self.x), int(self.y)),
            max(1, self.size)
        )


class ParticleManager:
    def __init__(self):
        self.particles = []

    # =====================================
    # Add Particle
    # =====================================
    def add_particle(self, x, y, colour=WHITE, size=3, life=30):
        if len(self.particles) >= MAX_PARTICLES:
            return

        self.particles.append(
            Particle(x, y, colour, size, life)
        )

    # =====================================
    # Update
    # =====================================
    def update(self):
        for particle in self.particles[:]:
            particle.update()

            if particle.life <= 0:
                self.particles.remove(particle)

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)


# =====================================================
# Effects
# =====================================================

def snow_effect(system):
    system.add_particle(
        random.randint(0, WIDTH),
        0,
        WHITE,
        2,
        random.randint(80, 120)
    )


def fire_effect(system):
    system.add_particle(
        random.randint(0, WIDTH),
        HEIGHT,
        ORANGE,
        random.randint(2, 5),
        random.randint(40, 80)
    )


def sparkle(system, x, y):
    for _ in range(12):
        system.add_particle(
            x,
            y,
            YELLOW,
            random.randint(2, 4),
            random.randint(25, 45)
        )


def portal_glow(system, rect):
    for _ in range(3):
        system.add_particle(
            random.randint(rect.left, rect.right),
            random.randint(rect.top, rect.bottom),
            CYAN,
            random.randint(2, 4),
            random.randint(30, 60)
        )


# ==========================================
# Compatibility Function
# ==========================================

def create_particles():
    return ParticleManager()