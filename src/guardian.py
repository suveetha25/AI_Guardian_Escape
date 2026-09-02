"""
=========================================
AI Guardian Escape
guardian.py

Guardian Artificial Intelligence

Implements

• Finite State Machine
• Patrol
• Chase
• Search
• Return
=========================================
"""

import math
import random
import pygame

from settings import *
from utils import distance


class Guardian:
    def __init__(self, level):
        self.level = level

        self.width = GUARDIAN_SIZE
        self.height = GUARDIAN_SIZE

        self.state = PATROL
        self.direction = random.choice([-1, 1])

        self.speed = PATROL_SPEED[level]
        self.chase_speed = CHASE_SPEED[level]
        self.current_speed = self.speed

        self.search_timer = SEARCH_TIME
        self.last_known_position = None
        self.player_visible = False

        self.anim_time = random.uniform(0, 3)

        if level == FOREST:
            self.detection_radius = 140
            self.attack_radius = 28
        elif level == CASTLE:
            self.detection_radius = 170
            self.attack_radius = 30
        elif level == SNOW:
            self.detection_radius = 200
            self.attack_radius = 32
        else:
            self.detection_radius = 230
            self.attack_radius = 34

        patrol_width = 440
        start_x = random.randint(WIDTH - 560, WIDTH - 140)
        self.patrol_left = max(80, start_x - patrol_width // 2)
        self.patrol_right = min(WIDTH - 60, self.patrol_left + patrol_width)

        if self.patrol_right - self.patrol_left < patrol_width:
            self.patrol_left = self.patrol_right - patrol_width

        spawn_x = random.randint(self.patrol_left, max(self.patrol_left, self.patrol_right - self.width))
        spawn_y = random.randint(120, HEIGHT - 120 - self.height)

        self.spawn_point = (spawn_x, spawn_y)

        self.rect = pygame.Rect(
            spawn_x,
            spawn_y,
            self.width,
            self.height
        )

    # =====================================
    # Player Detection
    # =====================================
    def detect_player(self, player):
        if player.is_invisible:
            self.player_visible = False
            return False

        d = distance(
            self.rect.center,
            player.rect.center
        )

        self.player_visible = d <= self.detection_radius
        return self.player_visible

    # =====================================
    # Patrol
    # =====================================
    def patrol(self):
        self.current_speed = self.speed
        self.rect.x += self.direction * self.current_speed

        if self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1
        elif self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1

        self.anim_time += 0.08

    # =====================================
    # Chase
    # =====================================
    def chase(self, player):
        self.current_speed = self.chase_speed
        self.last_known_position = player.rect.center

        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.current_speed
        elif player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.current_speed

        if player.rect.centery > self.rect.centery:
            self.rect.y += self.current_speed
        elif player.rect.centery < self.rect.centery:
            self.rect.y -= self.current_speed

        self.rect.left = max(40, self.rect.left)
        self.rect.right = min(WIDTH - 40, self.rect.right)
        self.rect.top = max(40, self.rect.top)
        self.rect.bottom = min(HEIGHT - 40, self.rect.bottom)

        self.anim_time += 0.18

    # =====================================
    # Search
    # =====================================
    def search(self):
        if self.last_known_position is None:
            self.state = RETURN
            return

        target_x, target_y = self.last_known_position

        if abs(target_x - self.rect.centerx) > 5:
            if target_x > self.rect.centerx:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        if abs(target_y - self.rect.centery) > 5:
            if target_y > self.rect.centery:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed

        self.search_timer -= 1
        self.anim_time += 0.1

        if self.search_timer <= 0:
            self.search_timer = SEARCH_TIME
            self.state = RETURN

    # =====================================
    # Return
    # =====================================
    def return_to_patrol(self):
        target_x, target_y = self.spawn_point

        if abs(self.rect.x - target_x) > 5:
            if self.rect.x < target_x:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        if abs(self.rect.y - target_y) > 5:
            if self.rect.y < target_y:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed

        self.anim_time += 0.08

        if abs(self.rect.x - target_x) <= 5 and abs(self.rect.y - target_y) <= 5:
            self.rect.x = target_x
            self.rect.y = target_y
            self.state = PATROL

    # =====================================
    # Update FSM
    # =====================================
    def update(self, player, walls):
        seen = self.detect_player(player)

        if self.state == PATROL:
            self.patrol()
            if seen:
                self.state = CHASE

        elif self.state == CHASE:
            if seen:
                self.chase(player)
            else:
                self.state = SEARCH

        elif self.state == SEARCH:
            self.search()
            if seen:
                self.state = CHASE

        elif self.state == RETURN:
            self.return_to_patrol()
            if seen:
                self.state = CHASE

    # =====================================
    # Collision
    # =====================================
    def caught_player(self, player):
        d = distance(
            self.rect.center,
            player.rect.center
        )
        return d <= self.attack_radius

    # =====================================
    # Draw
    # =====================================
    def draw(self, screen):
        is_alert = self.state == CHASE
        base = (230, 80, 80) if is_alert else (80, 220, 120)
        dark = (120, 20, 20) if is_alert else (20, 110, 45)
        glow = (255, 90, 90, 70) if is_alert else (90, 255, 160, 70)

        bob = int(math.sin(self.anim_time * 3.5) * 3)
        draw_rect = self.rect.copy()
        draw_rect.y += bob

        surf = pygame.Surface((draw_rect.width + 28, draw_rect.height + 28), pygame.SRCALPHA)
        cx = surf.get_width() // 2
        cy = surf.get_height() // 2

        for r in (24, 19, 14):
            pygame.draw.circle(surf, glow, (cx, cy), r)

        pygame.draw.ellipse(surf, (0, 0, 0, 40), (cx - 12, cy + 13, 24, 8))

        body = pygame.Rect(cx - 12, cy - 9, 24, 24)
        pygame.draw.ellipse(surf, base, body)
        pygame.draw.ellipse(surf, dark, body, 2)

        left_ear = [(cx - 8, cy - 6), (cx - 14, cy - 16), (cx - 4, cy - 11)]
        right_ear = [(cx + 8, cy - 6), (cx + 14, cy - 16), (cx + 4, cy - 11)]
        pygame.draw.polygon(surf, base, left_ear)
        pygame.draw.polygon(surf, base, right_ear)
        pygame.draw.polygon(surf, dark, left_ear, 2)
        pygame.draw.polygon(surf, dark, right_ear, 2)

        pygame.draw.circle(surf, WHITE, (cx - 5, cy - 1), 3)
        pygame.draw.circle(surf, WHITE, (cx + 5, cy - 1), 3)
        pygame.draw.circle(surf, dark, (cx - 5, cy - 1), 1)
        pygame.draw.circle(surf, dark, (cx + 5, cy - 1), 1)

        pygame.draw.arc(surf, dark, (cx - 5, cy + 2, 10, 6), 0.1, 3.1, 2)

        wisp_points = [
            (cx - 10, cy + 12),
            (cx - 4, cy + 19),
            (cx, cy + 14),
            (cx + 4, cy + 20),
            (cx + 10, cy + 12)
        ]
        pygame.draw.polygon(surf, base, wisp_points)
        pygame.draw.polygon(surf, dark, wisp_points, 2)

        screen.blit(surf, (draw_rect.x - 14, draw_rect.y - 14))

        if SHOW_DETECTION_RADIUS:
            pygame.draw.circle(
                screen,
                YELLOW,
                self.rect.center,
                self.detection_radius,
                1
            )