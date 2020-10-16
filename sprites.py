#Sprite file
import random
import pygame as pg
from settings import *

vec = pg.math.Vector2
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,70))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.center = (0,0)
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.pos = vec(WIDTH / 2,HEIGHT / 2)
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = 0-PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width,height))
        self.image.fill((0,random.randrange(100,255),0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
