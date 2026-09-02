"""
=========================================
AI Guardian Escape
The Magical Worlds

settings.py

Global Constants
=========================================
"""

# ==========================================
# SCREEN
# ==========================================

WIDTH = 1280
HEIGHT = 720
FPS = 60

TITLE = "AI Guardian Escape : The Magical Worlds"

# ==========================================
# GAME STATES
# ==========================================

SPLASH = "SPLASH"
MENU = "MENU"
MAP = "MAP"
HELP = "HELP"
SETTINGS_MENU = "SETTINGS"
SETTINGS = SETTINGS_MENU
PLAYING = "PLAYING"
PAUSE = "PAUSE"
LEVEL_COMPLETE = "LEVEL_COMPLETE"
GAME_OVER = "GAME_OVER"
CONGRATULATIONS = "CONGRATULATIONS"
CREDITS = "CREDITS"

# ==========================================
# LEVEL IDS
# ==========================================

FOREST = 1
CASTLE = 2
SNOW = 3
VOLCANO = 4

# ==========================================
# PLAYER
# ==========================================

PLAYER_SIZE = 32
PLAYER_SPEED = 5
PLAYER_RUN_SPEED = 8
PLAYER_MAX_HEALTH = 3
PLAYER_COLOR = (50, 120, 255)

# ==========================================
# GUARDIAN
# ==========================================

GUARDIAN_SIZE = 36

PATROL = "PATROL"
CHASE = "CHASE"
SEARCH = "SEARCH"
RETURN = "RETURN"

DETECTION_RADIUS = 220
SEARCH_TIME = 180

PATROL_SPEED = {
    FOREST: 2,
    CASTLE: 3,
    SNOW: 4,
    VOLCANO: 5
}

CHASE_SPEED = {
    FOREST: 3,
    CASTLE: 4,
    SNOW: 5,
    VOLCANO: 6
}

# ==========================================
# COLLECTIBLES
# ==========================================

COLLECTIBLE_SIZE = 20

COLLECTIBLE_COUNTS = {
    FOREST: 6,
    CASTLE: 5,
    SNOW: 4,
    VOLCANO: 3
}

# ==========================================
# PORTAL
# ==========================================

PORTAL_WIDTH = 50
PORTAL_HEIGHT = 70

# ==========================================
# LEVEL TIMER
# ==========================================

LEVEL_TIME = {
    FOREST: 180,
    CASTLE: 170,
    SNOW: 160,
    VOLCANO: 150
}

# ==========================================
# POWERUPS
# ==========================================

POWERUP_SIZE = 24
POWERUP_DURATION = 8
INVISIBILITY_TIME = 5
TIME_CRYSTAL_BONUS = 20

# ==========================================
# PARTICLES
# ==========================================

MAX_PARTICLES = 300

# ==========================================
# UI
# ==========================================

FONT_SIZE = 24
TITLE_SIZE = 52
HUD_MARGIN = 15

# ==========================================
# COLOURS
# ==========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (220, 60, 60)
GREEN = (60, 220, 60)
BLUE = (60, 120, 255)

YELLOW = (255, 220, 0)
CYAN = (0, 255, 255)
PURPLE = (180, 80, 255)
ORANGE = (255, 140, 0)

GREY = (120, 120, 120)
LIGHT_GREY = (220, 220, 220)

FOREST_BG = (80, 165, 80)
CASTLE_BG = (145, 145, 165)
SNOW_BG = (225, 240, 255)
VOLCANO_BG = (130, 45, 20)

# ==========================================
# DEBUG
# ==========================================

DEBUG = False
SHOW_COLLIDERS = False
SHOW_PATH = False
SHOW_DETECTION_RADIUS = False