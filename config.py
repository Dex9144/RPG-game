import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
CROP_SIZE = 32
FPS = 60

PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCKS_LAYER = 2
GROUND_LAYER = 1

BLACK = (0, 0, 0)
WHITE = (0, 0, 0)

PLAYER_STEPS = 4
ENEMY_STEPS = 1

tile_map = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B....P.............B",
    "B............E.....B",
    "B...BBB............B",
    "B..................B",
    "B..................B",
    "B.........BBB......B",
    "B..................B",
    "B..................B",
    "B.........B........B",
    "B..BBB.............B",
    "B.........E........B",
    "B...............BBBB",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB",
    "B"
]