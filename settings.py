# game options/settings
import os
import pygame as pg
TITLE = "A Day in Life"
WIDTH = 1000
HEIGHT = 600
FPS = 60

GAME_FOLDER = os.path.dirname(__file__)


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (0, 255, 0)
BLUE = (0, 200, 255)
YELLOW = (255, 255, 0)
BROWN = (200,200,100)
GREY = (150,150,150)

#PLAYER_PROPERTIES
PLAYER_ACC = 2
PLAYER_GRAV = 1
PLAYER_FRIC = -0.22

FONT_NAME = pg.font.match_font('comic sans ms')
