"""
=========================================
AI Guardian Escape
levels.py

Stores all level layouts and properties.
=========================================
"""

import pygame

from settings import *


LEVELS = {

    FOREST: {

        "name": "Enchanted Forest",

        "background": FOREST_BG,

        "guardian_name": "Barkon",

        "difficulty": "Easy",

        "collectible_type": "flower",

        "portal": pygame.Rect(
            WIDTH - 80,
            HEIGHT - 120,
            PORTAL_WIDTH,
            PORTAL_HEIGHT
        ),

        "walls": [

            pygame.Rect(180,120,40,220),
            pygame.Rect(350,0,40,300),
            pygame.Rect(520,180,40,260),
            pygame.Rect(720,80,40,260),
            pygame.Rect(900,250,40,250)

        ],

        "collectibles":[

            (100,100),
            (250,500),
            (470,120),
            (650,520),
            (870,120),
            (1080,420)

        ]

    },

    CASTLE: {

        "name":"Magic Castle",

        "background":CASTLE_BG,

        "guardian_name":"Sir Lumis",

        "difficulty":"Medium",

        "collectible_type":"crystal",

        "portal":pygame.Rect(

            WIDTH-80,
            HEIGHT-120,
            PORTAL_WIDTH,
            PORTAL_HEIGHT

        ),

        "walls":[

            pygame.Rect(150,150,700,30),

            pygame.Rect(300,150,30,350),

            pygame.Rect(520,250,30,320),

            pygame.Rect(800,120,30,350),

            pygame.Rect(920,420,220,30)

        ],

        "collectibles":[

            (120,80),
            (380,620),
            (620,320),
            (900,180),
            (1120,580)

        ]

    },

    SNOW:{

        "name":"Snow Kingdom",

        "background":SNOW_BG,

        "guardian_name":"Frost Wisp",

        "difficulty":"Hard",

        "collectible_type":"ice",

        "portal":pygame.Rect(

            WIDTH-80,
            HEIGHT-120,
            PORTAL_WIDTH,
            PORTAL_HEIGHT

        ),

        "walls":[

            pygame.Rect(220,80,40,250),

            pygame.Rect(420,260,320,40),

            pygame.Rect(760,80,40,350),

            pygame.Rect(980,300,180,40)

        ],

        "collectibles":[

            (100,120),
            (350,500),
            (720,220),
            (1060,520)

        ]

    },

    VOLCANO:{

        "name":"Volcano Realm",

        "background":VOLCANO_BG,

        "guardian_name":"Inferno Sentinel",

        "difficulty":"Expert",

        "collectible_type":"brick",

        "portal":pygame.Rect(

            WIDTH-80,
            HEIGHT-120,
            PORTAL_WIDTH,
            PORTAL_HEIGHT

        ),

        "walls":[

            pygame.Rect(180,180,500,40),

            pygame.Rect(680,180,40,320),

            pygame.Rect(860,420,260,40),

            pygame.Rect(980,80,40,240)

        ],

        "collectibles":[

            (120,620),
            (650,320),
            (1080,120)

        ]

    }

}