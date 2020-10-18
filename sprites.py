#Sprite file
import random
import pygame as pg
from settings import *

corona_radius = pg.image.load(os.path.join(GAME_FOLDER,'corona_radius.png'))
vec = pg.math.Vector2
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,70))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.center = (WIDTH / 2,0)
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.pos = vec(WIDTH / 2,HEIGHT / 2)
        self.game = game
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
        self.rect.bottom = self.pos.y
    def jump(self,pow):
        self.rect.y += 1
        self.platcols = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.y -= 1
        if self.platcols:
            self.vel.y = -pow

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height,bounce,game,stationary=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width,height))
        self.image.fill(random.choice([GREEN,BROWN,GREY]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.bounce = bounce
        self.game = game
        self.pos = vec(x,y)
        self.active = False
        self.stationary = stationary
        self.lost = True
        self.width = width
    def update(self):
        if not self.stationary:
            self.pos.x += -self.game.player.vel.x + 0.5 * self.game.player.acc.x
            self.rect.bottomleft = self.pos
        if self.rect.left < 0:
            self.active = True

class Person(pg.sprite.Sprite):
    def __init__(self,game,platform):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,70))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.radius = random.randrange(70,200)
        #pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.platform = platform
        self.rect.midbottom = self.platform.rect.midtop
        self.ppoint = vec(self.platform.rect.centerx,self.platform.rect.top)
        self.pos = vec(0,0)
        self.speed = 2

    def update(self):
        # if self.rect.right > self.platform.rect.right:
        #     self.speed = 0 - self.speed
        #     print(self.speed)
        # if self.rect.left < self.platform.rect.left:
        #     self.speed = 0 - self.speed
        #     print(2)
        # self.pos.x += self.speed
        self.rect.midbottom = self.platform.rect.midtop
        #pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        # print(1)
class Radiusc(pg.sprite.Sprite):
    def __init__(self,person):
        pg.sprite.Sprite.__init__(self)
        self.person = person
        self.image = pg.transform.scale(corona_radius.convert(),(self.person.radius *2,self.person.radius*2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.person.rect.center
    def update(self):
        self.rect.center = self.person.rect.center
