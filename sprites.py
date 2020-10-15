#Sprite file
import random
import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,70))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.center = (WIDTH)
