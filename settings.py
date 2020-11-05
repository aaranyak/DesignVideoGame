# game options/settings
import os
import pygame as pg
TITLE = "A Day in Life"
WIDTH = 1000
HEIGHT = 600
FPS = 60

explode = []
GAME_FOLDER = os.path.dirname(__file__)
MUSIC_FOLDER = os.path.join(GAME_FOLDER,'Music')
IMAGE_FOLDER = os.path.join(GAME_FOLDER,'Pictures')

PLAYER_SPRITESHEET = os.path.join(IMAGE_FOLDER,'player_spritesheet.png')
POWERUPS = {'sanitizer' : os.path.join(IMAGE_FOLDER,'sanitizer.png'),'mask' : os.path.join(IMAGE_FOLDER,'Mask.png'),'coin':os.path.join(IMAGE_FOLDER,'covid.png')}
PROPS = [os.path.join(IMAGE_FOLDER,'House.png'),os.path.join(IMAGE_FOLDER,'Bush.png'),os.path.join(IMAGE_FOLDER,'Tree1.png'),os.path.join(IMAGE_FOLDER,'Tree2.png')]
HEALTH_RATE = 21
clouds = []
for i in range(4):
    s = os.path.join(IMAGE_FOLDER,'clou'+str(i)+'.png')
    clouds.append(s)
CLOUDS = clouds
for i in range(35):
    if i < 10:
        explode.append(os.path.join(IMAGE_FOLDER,'particle000'+str(i)+'.png'))
    else:
        explode.append(os.path.join(IMAGE_FOLDER,'particle00'+str(i)+'.png'))
EXPLODE = explode

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

FONT_NAME = pg.font.match_font('ubuntu')
