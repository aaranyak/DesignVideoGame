import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def hit_ground(self):
        self.platcols = pg.sprite.spritecollide(self.player, self.platforms,False)
        if self.platcols:
            if self.player.vel.y >= 0:
                self.player.pos.y = self.platcols[0].rect.top
                self.player.vel.y = 0- self.player.vel.y / self.platcols[0].bounce
    def draw_text(self,surf,text,size,x,y,color):
        self.font = pg.font.Font(FONT_NAME,size)
        self.text_surf = self.font.render(text, True , color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.topleft = (x, y)
        surf.blit(self.text_surf, self.text_rect)

    def draw_progress_bar(self,surf,color,outiline,x,y,w,h,pct,textcol):
        self.pct = pct
        if self.pct < 0:
            self.pct = 0
        self.outline = pg.Rect(x,y,w,h)
        self.fill = pg.Rect(x,y,int(float(pct) / 100.0 * float(w)),h)
        pg.draw.rect(surf,color,self.fill)
        pg.draw.rect(surf,outiline,self.outline,2)
        self.draw_text(surf,str(int(pct)) + "%",h-3,x,y,textcol)

    def spawn_platforms(self):
        self.ground = Platform(0,HEIGHT,WIDTH,30,10,self,stationary=True)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)
        for i in range(8):
            self.w = random.randrange(10,300)
            self.x = random.randrange(0,WIDTH)
            self.y = random.randrange(0,HEIGHT)
            self.p = Platform(self.x,self.y,self.w,20,random.randrange(1,5),self)
            self.all_sprites.add(self.p)
            self.platforms.add(self.p)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.people = pg.sprite.Group()
        #Spawn sprites
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.spawn_platforms()
        self.health = 100.0
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.hit_ground()
        self.losts = 0
        for plat in self.platforms:
            if plat.active and plat.lost:
                self.losts += 1
                plat.lost = False
        for i in range(self.losts):
            self.w = random.randrange(100,500)
            self.x = random.randrange(WIDTH,WIDTH*2)
            self.y = random.randrange(0,HEIGHT)
            self.p = Platform(self.x,self.y,self.w,20,random.randrange(2,10),self)
            self.all_sprites.add(self.p)
            self.platforms.add(self.p)
            if random.random() > 0.7:
                self.m = Person(self,self.p,random.choice([False,True]))
                self.all_sprites.add(self.m)
                self.people.add(self.m)
                self.d = Radiusc(self.m)
                self.all_sprites.add(self.d)
        self.distance = pg.sprite.spritecollide(self.player,self.people,False,pg.sprite.collide_circle)
        if self.distance:
            self.health -= 3 / FPS






    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump(30)
        if self.health < 0:
            self.running = False
            quit()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_progress_bar(self.screen,GREEN,BROWN,130,5,300,30,self.health,BLACK)
        self.draw_text(self.screen,"Health =", 30,3,3,BLACK)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
quit()
