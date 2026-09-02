"""
=========================================
AI Guardian Escape
utils.py

Utility functions used throughout
the project.
=========================================
"""

import math
import heapq
import pygame


# ==========================================
# Distance
# ==========================================

def distance(point1, point2):
    """
    Euclidean Distance
    """

    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


# ==========================================
# Manhattan Distance
# Used by A* Search
# ==========================================

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ==========================================
# Rectangle Center
# ==========================================

def rect_center(rect):

    return (
        rect.centerx,
        rect.centery
    )


# ==========================================
# Clamp Value
# ==========================================

def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


# ==========================================
# Draw Text
# ==========================================

def draw_text(
    surface,
    text,
    font,
    colour,
    x,
    y
):

    image = font.render(
        str(text),
        True,
        colour
    )

    surface.blit(image, (x, y))


# ==========================================
# Draw Center Text
# ==========================================

def draw_center_text(
    surface,
    text,
    font,
    colour,
    y
):

    image = font.render(
        str(text),
        True,
        colour
    )

    x = (
        surface.get_width()
        - image.get_width()
    ) // 2

    surface.blit(
        image,
        (x, y)
    )


# ==========================================
# Grid Conversion
# ==========================================

GRID_SIZE = 40


def world_to_grid(x, y):

    return (
        x // GRID_SIZE,
        y // GRID_SIZE
    )


def grid_to_world(col, row):

    return (
        col * GRID_SIZE + GRID_SIZE // 2,
        row * GRID_SIZE + GRID_SIZE // 2
    )


# ==========================================
# A* Search Algorithm
# ==========================================

def astar(start, goal, blocked):

    open_set = []

    heapq.heappush(
        open_set,
        (0, start)
    )

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: heuristic(start, goal)
    }

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.reverse()

            return path

        neighbours = [

            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)

        ]

        for neighbour in neighbours:

            if neighbour in blocked:
                continue

            tentative = g_score[current] + 1

            if neighbour not in g_score or tentative < g_score[neighbour]:

                came_from[neighbour] = current

                g_score[neighbour] = tentative

                f_score[neighbour] = (
                    tentative +
                    heuristic(neighbour, goal)
                )

                heapq.heappush(
                    open_set,
                    (
                        f_score[neighbour],
                        neighbour
                    )
                )

    return []


# ==========================================
# Hill Climbing
# Adaptive Difficulty
# ==========================================

def hill_climb(
    guardian_speed,
    player_wins,
    player_losses
):

    if player_wins > player_losses:

        guardian_speed += 0.2

    elif player_losses > player_wins:

        guardian_speed -= 0.2

    guardian_speed = clamp(
        guardian_speed,
        2,
        8
    )

    return guardian_speed