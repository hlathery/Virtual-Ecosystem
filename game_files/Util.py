TILESHEET_PATH = "Assets/better-tileset.png"
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1400
FPS = 60
WINDOW_WIDTH    = 1920
WINDOW_HEIGHT   = 1080
TILESIZE        = 16       # tile width/height in pixels in tilesheet
WORLD_X         = (WINDOW_WIDTH + TILESIZE - 1) // TILESIZE
WORLD_Y         = (WINDOW_HEIGHT + TILESIZE - 1) // TILESIZE


# Terrain types
OCEAN3 = 0
OCEAN2 = 1
OCEAN1 = 2
BEACH = 3
GRASS = 4
FOREST = 5


# List of all terrain type, ordered from lower height to higher height
ALL_TERRAIN_TYPES = [OCEAN3, OCEAN2, OCEAN1, BEACH, GRASS, FOREST]


# All tiles in the tilesheet, for each terrain type in ALL_TERRAIN_TYPES
TERRAIN_TILES = [
    # Ocean depth level 3 tiles
    [
        (0, 0),  #
        (352, 160),  ## bottom-right
        (384, 160),  ## bottom-left
        (368, 160),  ## bottom side
        (352, 192),  ## top-right
        (352, 176),  ## right side
        (400, 144),  ## TR, BL
        (400, 160),  ## TR, BL, BR
        (384, 192),  ## top-left
        (416, 144),  ## TL, BR
        (384, 176),  ## left side
        (416, 208),  ## TL + BL + BR
        (368, 192),  ## top side
        (368, 176),  ## TL + TR + BR
        (416, 224),  ## TL + TR + BL
        (368, 176),  ## all sides
    ],
    # Ocean depth level 2 tiles
    [
        (0, 0),  #
        (272, 160),  ## bottom-right
        (304, 160),  ## bottom-left
        (288, 160),  ## bottom side
        (272, 192),  ## top-right
        (272, 176),  ## right side
        (336, 144),  ## TR, BL
        (320, 160),  ## TR, BL, BR
        (304, 192),  ## top-left
        (352, 144),  ## TL, BR
        (304, 176),  ## left side
        (336, 160),  ## TL + BL + BR
        (288, 192),  ## top side
        (320, 176),  ## TL + TR + BR
        (336, 176),  ## TL + TR + BL
        (288, 176),  ## all sides
    ],
    # Ocean depth level 1 tiles
    [
        (0, 0),  #
        (192, 160),  ## bottom-right
        (224, 160),  ## bottom-left
        (208, 160),  ## bottom side
        (192, 192),  ## top-right
        (192, 176),  ## right side
        (288, 144),  ## TR, BL
        (240, 160),  ## TR, BL, BR
        (224, 192),  ## top-left
        (304, 144),  ## TL, BR
        (224, 176),  ## left side
        (256, 160),  ## TL + BL + BR
        (208, 192),  ## top side
        (240, 176),  ## TL + TR + BR
        (256, 176),  ## TL + TR + BL
        (208, 176),  ## all sides
    ],
    # Beach level tiles
    [
        (0, 0),  #
        (352, 0),  ## bottom-right
        (192, 0),  ## bottom-left
        (176, 0),  ## bottom side
        (160, 32),  ## top-right
        (160, 16),  ## right side
        (400, 32),  ## TR, BL
        (208, 0),  ## TR, BL, BR
        (192, 32),  ## top-left
        (416, 32),  # TR, BL
        (192, 16),  ## left side
        (224, 0),  ## TL + BL + BR
        (176, 32),  ## top side
        (208, 16),  ## TL + TR + BR
        (224, 16),  ## TL + TR + BL
        (176, 16),  ## all sides
    ],
    # Grass level tiles
    [
        (0, 0),  #
        (112, 128), ## bottom-right
        (96, 128), ## bottom-left
        (64, 144), ## bottom side
        (112, 112), ## top-right
        (80, 128), ## right side
        (112, 144), ## TR, BL
        (80, 144), ## TR, BL, BR
        (96, 112), ## top-left
        (96, 144), ## TL, BR
        (48, 128), ## left side
        (48, 144), ## TL + BL + BR
        (64, 112), ## top side
        (80, 112), ## TL + TR + BR
        (48, 112), ## TL + TR + BL
        (32, 32),  ## all sides
    ],
    # Forest level tiles
    [
        (0, 0),  #
        (112, 128), ## bottom-right
        (96, 128), ## bottom-left
        (64, 144), ## bottom side
        (112, 112), ## top-right
        (80, 128), ## right side
        (112, 144), ## TR, BL
        (80, 144), ## TR, BL, BR
        (96, 112), ## top-left
        (96, 144), ## TL, BR
        (48, 128), ## left side
        (48, 144), ## TL + BL + BR
        (64, 112), ## top side
        (80, 112), ## TL + TR + BR
        (48, 112), ## TL + TR + BL
        (64, 128), ## all sides
    ]
]