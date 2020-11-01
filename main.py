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
        self.start_screen_sprites = pg.sprite.Group()
        self.end_screen_sprites = pg.sprite.Group()
        self.playbutton = Button(WIDTH / 2,500,150,70,(0,170,0),GREEN)
        self.playagbutton = Button(WIDTH / 2,500,200,70,(0,170,0),GREEN)
        self.start_screen_sprites.add(self.playbutton)
        self.end_screen_sprites.add(self.playagbutton)
        self.level = 0

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
    def draw_text_center(self,surf,text,size,x,y,color):
        self.font = pg.font.Font(FONT_NAME,size)
        self.text_surf = self.font.render(text, True , color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (x, y)
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
            self.p = Platform(self.x,self.y,self.w,20,10,self)
            self.all_sprites.add(self.p)
            self.platforms.add(self.p)

    def new(self):
        # start a new game
        self.game_over = False
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.people = pg.sprite.Group()
        self.start_screen_sprites = pg.sprite.Group()
        self.end_screen_sprites = pg.sprite.Group()
        self.corona_radiuses = pg.sprite.Group()
        self.player_spritesheet = SpriteSheet(PLAYER_SPRITESHEET,7,2,446,793,BLACK)
        self.guy2image = [pg.image.load(os.path.join(os.path.join(IMAGE_FOLDER,'Cars'),'guy2.png')).convert_alpha(),pg.image.load(os.path.join(os.path.join(IMAGE_FOLDER,'Cars'),'guy3.png')).convert_alpha()]
        self.cars = [pg.image.load(os.path.join(os.path.join(IMAGE_FOLDER,'Cars'),'car1.png')).convert_alpha(),pg.image.load(os.path.join(os.path.join(IMAGE_FOLDER,'Cars'),'car2.png')).convert_alpha()]
        #Spawn sprites
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.spawn_platforms()
        self.health = 100.0
        self.jump_sound = pg.mixer.Sound(os.path.join(MUSIC_FOLDER,'phaseJump2.wav'))
        self.lose_sound = pg.mixer.Sound(os.path.join(MUSIC_FOLDER,'zapThreeToneDown.wav'))
        self.win_sound = pg.mixer.Sound(os.path.join(MUSIC_FOLDER,'coin.wav'))
        pg.mixer.music.load(os.path.join(MUSIC_FOLDER,'NaughtyNess.ogg'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(100)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.corona_radiuses.update()
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
                self.corona_radiuses.add(self.d)
        self.distance = pg.sprite.spritecollide(self.player,self.corona_radiuses,False,pg.sprite.collide_mask)
        if self.distance:
            self.health -= 12 / FPS







    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump(30)
        if self.health < 0:
            self.game_over = True
            self.lose_sound.play()
            self.playing = False
        elif len(self.platforms) > 8 * 4 + 8 * self.level:
            self.game_over = False
            self.win_sound.play()
            self.playing = False


    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        for corona in self.corona_radiuses:
            self.screen.blit(corona.image,corona.rect)
        self.people.draw(self.screen)
        self.draw_progress_bar(self.screen,GREEN,BROWN,130,5,300,30,self.health,BLACK)
        self.draw_text(self.screen,"Health =", 30,3,3,BLACK)
        self.draw_text_center(self.screen,"You are on level " + str(self.level),30,WIDTH / 2, 40,RED)
        for person in self.people:
            self.draw_text_center(self.screen,"Keep Distance (Or Else!)",20,person.rect.centerx,person.rect.top,GREEN)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(os.path.join(MUSIC_FOLDER,'Chase.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLUE)
        self.draw_text_center(self.screen,TITLE,50,WIDTH/2,HEIGHT/2 - 200,GREEN)
        self.draw_text_center(self.screen,""" Welcome to Day in Life""",30,WIDTH/2,HEIGHT/2 - 100,RED)
        self.draw_text_center(self.screen,""" This is a video game where you learn to survive""",20,WIDTH/2,HEIGHT/2 - 65,RED)
        self.draw_text_center(self.screen,""" in a daily life routine.""",20,WIDTH/2,HEIGHT/2 - 45,RED)
        self.draw_text_center(self.screen,""" Keep social distance from other people and keep your mask on""",20,WIDTH/2,HEIGHT/2 - 25,RED)
        self.draw_text_center(self.screen,""" and don't forget to sanitize your hands whenever you can.""",20,WIDTH/2,HEIGHT/2 - 5,RED)
        self.draw_text_center(self.screen,""" Use your arrow keys to move and spacebar to jump!""",20,WIDTH/2,HEIGHT/2 + 15,RED)
        self.draw_text_center(self.screen,""" Have Fun!""",25,WIDTH/2,HEIGHT/2 + 40,RED)
        self.wait_for_key(self.playbutton,True)
        pg.mixer.music.fadeout(100)



    def show_go_screen(self):
        # game over/continue
        pg.mixer.music.load(os.path.join(MUSIC_FOLDER,'Em-Poms-.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLUE)
        self.end_screen_sprites.draw(self.screen)
        self.draw_text_center(self.screen,TITLE,50,WIDTH/2,HEIGHT/2 - 200,GREEN)
        self.draw_text_center(self.screen,""" Remember, this is day in life.""",30,WIDTH/2,HEIGHT/2 - 100,RED)
        self.draw_text_center(self.screen,""" This is a video game where you learn to survive""",20,WIDTH/2,HEIGHT/2 - 65,RED)
        self.draw_text_center(self.screen,""" in a daily life routine.""",20,WIDTH/2,HEIGHT/2 - 45,RED)
        self.draw_text_center(self.screen,""" Keep social distance from other people and keep your mask on""",20,WIDTH/2,HEIGHT/2 - 25,RED)
        self.draw_text_center(self.screen,""" and don't forget to sanitize your hands whenever you can.""",20,WIDTH/2,HEIGHT/2 - 5,RED)
        self.draw_text_center(self.screen,""" Use your arrow keys to move and spacebar to jump!""",20,WIDTH/2,HEIGHT/2 + 15,RED)
        self.draw_text_center(self.screen,""" Have Fun!""",25,WIDTH/2,HEIGHT/2 + 40,RED)
        self.playagbutton = Button(WIDTH / 2,500,200,70,(0,170,0),GREEN)
        self.end_screen_sprites.add(self.playagbutton)
        self.wait_for_key(self.playagbutton,False)
        pg.mixer.music.fadeout(100)
    def show_win_screen(self):
        pg.mixer.music.load(os.path.join(MUSIC_FOLDER,'Chase.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLUE)
        self.end_screen_sprites.draw(self.screen)
        self.draw_text_center(self.screen,"You Win!",50,WIDTH/2,HEIGHT/2 - 200,GREEN)
        self.draw_text_center(self.screen,"Time to advance to level "+str(self.level+1)+"!",30,WIDTH/2,HEIGHT/2 - 100,RED)
        self.draw_text_center(self.screen,""" This is a video game where you learn to survive""",20,WIDTH/2,HEIGHT/2 - 65,RED)
        self.draw_text_center(self.screen,""" in a daily life routine.""",20,WIDTH/2,HEIGHT/2 - 45,RED)
        self.draw_text_center(self.screen,""" Keep social distance from other people and keep your mask on""",20,WIDTH/2,HEIGHT/2 - 25,RED)
        self.draw_text_center(self.screen,""" and don't forget to sanitize your hands whenever you can.""",20,WIDTH/2,HEIGHT/2 - 5,RED)
        self.draw_text_center(self.screen,""" Use your arrow keys to move and spacebar to jump!""",20,WIDTH/2,HEIGHT/2 + 15,RED)
        self.draw_text_center(self.screen,""" Have Fun!""",25,WIDTH/2,HEIGHT/2 + 40,RED)
        self.wait_for_key(self.playbutton,True)
        pg.mixer.music.fadeout(100)
        self.level += 1
    def wait_for_key(self,playevent,start):
        self.waiting = True
        self.start_sound = pg.mixer.Sound(os.path.join(MUSIC_FOLDER,'powerUp3.wav'))
        while self.waiting:
            if start:
                self.start_screen_sprites.draw(self.screen)
                self.screen.blit(playevent.image,playevent.rect)
                self.draw_text_center(self.screen,"Click to play!",20,WIDTH / 2,500,RED)
                playevent.update()
                self.start_screen_sprites.update()
            else:
                self.screen.blit(playevent.image,playevent.rect)
                self.draw_text_center(self.screen,"Click to play again!",20,WIDTH / 2,500,RED)
                self.end_screen_sprites.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN and playevent.mouse_hovered():
                    self.start_sound.play()
                    self.waiting = False
            self.clock.tick(FPS)
            pg.display.flip()


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    if g.game_over:
        g.show_go_screen()
    if not g.game_over:
        g.show_win_screen()
pg.quit()
quit()
