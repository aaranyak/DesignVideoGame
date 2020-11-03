#Sprite file
import random
import pygame as pg
from settings import *
vec = pg.math.Vector2
corona_radius = pg.image.load(os.path.join(IMAGE_FOLDER,'corona_radius.png'))
class SpriteSheet:
    def __init__(self, filename,w,h,imw,imh,colorkey):
        self.filename = filename
        self.spritesheet = pg.image.load(self.filename).convert_alpha()
        self.colorkey = colorkey
        self.width = w
        self.height = h
        self.imw = imw
        self.imh = imh
        self.images = self.calculate_images()
    def get_image(self):
        pass
    def calculate_images(self):
        self.listim = []
        for c in range(self.height):
            for i in range(self.width):
                image = pg.Surface((self.imw,self.imh))
                image.blit(self.spritesheet,(0,0),(i * self.imw,c * self.imh,self.imw,self.imh))
                image.set_colorkey(self.colorkey)
                self.listim.append(image)
        return self.listim

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(self.game.player_spritesheet.images[7],(60,120))
        self.run_count = 0
        self.spritesheet = self.game.player_spritesheet
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2,0)
        self.oldframe = 0
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.pos = vec(WIDTH / 2,HEIGHT / 2)
    def update(self):
        self.oldframe += 1
        if self.oldframe > 2:
            self.oldframe = 0
        self.set_image()
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
            self.game.jump_sound.play()
            self.vel.y = -pow
    def set_image(self):
        if self.run_count > 6:
            self.run_count = 0
        if self.vel.y < -3:
            self.image = pg.transform.scale(self.spritesheet.images[8],(60,120))
            self.run_count = 1
        elif self.vel.y > 3:
            self.image = pg.transform.scale(self.spritesheet.images[7],(60,120))
            self.run_count = 1
        else:
            self.image = pg.transform.scale(self.spritesheet.images[self.run_count],(60,120))
        if self.vel.x > 3 or self.vel.x < -3:
            if self.oldframe == 1:
                self.run_count += 1
        if self.vel.x < 0:
            self.image = pg.transform.flip(self.image,True,False)
        self.mask = pg.mask.from_surface(self.image)
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
    def __init__(self,game,platform,moving = False):
        pg.sprite.Sprite.__init__(self)
        if moving:
            self.image = pg.transform.scale(random.choice(game.cars),(100,50))
        else:
            self.image = pg.transform.scale(random.choice(game.guy2image),(40,160))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = random.randrange(70,200)
        #pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.platform = platform
        self.rect.midbottom = self.platform.rect.midtop
        self.ppoint = vec(self.platform.rect.centerx,self.platform.rect.top)
        self.pos = vec(0,0)
        self.movable = moving
        if moving:
            self.speed = -2
        else:
            self.speed = 0
        self.addx = 0

    def update(self):
        self.ppoint = vec(self.platform.rect.centerx,self.platform.rect.top)
        if self.rect.right > self.platform.rect.right or self.rect.left < self.platform.rect.left:
            self.speed = 0-self.speed
            if self.movable:
                self.image = pg.transform.flip(self.image,True,False)
        self.addx += self.speed
        self.rect.centerx = self.ppoint.x + self.addx
        self.rect.bottom = self.platform.rect.top
class Radiusc(pg.sprite.Sprite):
    def __init__(self,person):
        pg.sprite.Sprite.__init__(self)
        self.person = person
        self.image = pg.transform.scale(corona_radius.convert_alpha(),(self.person.radius *2,self.person.radius*2))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.person.rect.center
        self.mask = pg.mask.from_surface(self.image)
    def update(self):
        self.rect.center = self.person.rect.center
class Button(pg.sprite.Sprite):
    def __init__(self,x,y,w,h,color,hovercolor):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.color = color
        self.hovercolor = hovercolor
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def update(self):
        self.image.fill(self.color)
        if self.mouse_hovered():
            self.image.fill(self.hovercolor)
    def mouse_hovered(self):
        if pg.mouse.get_pos()[0] in range(self.rect.left,self.rect.right) and pg.mouse.get_pos()[1] in range(self.rect.top,self.rect.bottom):
            return True
        else:
            return False

class Powerup(pg.sprite.Sprite):
    def __init__(self,type,x,y,game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(POWERUPS[type])
        if type == 'sanitizer':
            self.image = pg.transform.scale(self.image,(50,50))
        elif type == 'mask':
            self.image = pg.transform.scale(self.image,(100,50))
        self.rect = self.image.get_rect()
        self.rect.center = ((x,y))
        self.pos = vec(x,y)
        self.type = type
        self.game = game
    def update(self):
        self.pos.x += -self.game.player.vel.x + 0.5 * self.game.player.acc.x
        self.rect.center = self.pos
class Explode(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(EXPLODE[0]).convert_alpha(),(50,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.count = 0
        self.game = game
    def update(self):
        self.pos.x += -self.game.player.vel.x + 0.5 * self.game.player.acc.x
        self.rect.center = self.pos
        self.count += 1
        if self.count < 33:
            self.image = pg.transform.scale(pg.image.load(EXPLODE[self.count]).convert_alpha(),(100,100))
            self.image.set_colorkey(BLACK)
        if self.count > 33:
            self.kill()
