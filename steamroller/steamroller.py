#!/usr/bin/env python3
import argparse
import pygame as pg
import random as r

## command line arguments
parser = argparse.ArgumentParser(description='Help the crazy hat to avoid being steamrolled by stars!')
parser.add_argument('--debug', '-d', type=int, default=0,
                    help='''
debug mode.  different number for different debug effects.  0: game mode (default)
                    ''')
args = parser.parse_args()
debug_code = args.debug

## init
pg.init()
pg.mixer.init()
pic = pg.image.load("minihullmyts.png")
redstar = pg.image.load("redstar.png")
yellowstar = pg.image.load("potato.png")
dynamite = pg.image.load("tnt.png")
fragment = pg.image.load("fragment.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaiyuituituit")
do = True
dist = 5
up = True
down = True
left = True
right = True
mup = False
mdown = False
mleft = False
mright = False
timer = pg.time.Clock()
lifes = 5
points = 0
## debug-dependent setup
## potentially add more stuff here, e.g. how velocity depends on level
## you can also add more debug codes
if debug_code == 0:
    def nextThreshold(distance, velocity):
        lvlLength = 600*velocity
        return distance + lvlLength
else:
    def nextThreshold(distance, velocity):
        lvlLength = 600
        return distance + lvlLength
distance = 0  # distance covered so far
lvl = 0  # game level
vel = 1  # scroll speed
threshold = nextThreshold(0, vel)  # next level threshold

## Screen initialization
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
player = pg.sprite.Group()
stars = pg.sprite.Group()
ystars = pg.sprite.Group()
tnt = pg.sprite.Group()
frag = pg.sprite.Group()
class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, mup, mdown, mleft, mright):
        if self.rect.y <= 0:
            up = False
        else:
            up = True
        if self.rect.y >= screenh-120:
            down = False
        else:
            down = True
        if self.rect.x <= 0:
            left = False
        else:
            left = True
        if self.rect.x >= screenw-148:
            right = False
        else:
            right = True
        if mup and up:
            self.rect.y -= dist 
        if mdown and down:
            self.rect.y += dist
        if mleft and left:
            self.rect.x -= dist
        if mright and right:
            self.rect.x += dist
    def getxy(self):
        return self.rect.x,self.rect.y
class Star(pg.sprite.Sprite):
    def __init__(self, x, vel, pic):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = screenh+100
        self.vel = vel
        #self.vel = vel
    def update(self, vel):
        self.rect.y -= vel*self.vel
        #self.rect.x += r.randint(-self.vel,self.vel)
        if self.rect.y < -10:
            stars.remove(self)
            ystars.remove(self)
class TNT(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = dynamite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.vel = vel
    def update(self):
        self.rect.y += 10
        if self.rect.y > screenh+10:
            tnt.remove(self)
class Frag(pg.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        pg.sprite.Sprite.__init__(self)
        self.image = fragment
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
        #self.vel = vel
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.y <= -10:
            frag.remove(self)
        elif self.rect.y >= screenh+10:
            frag.remove(self)
        elif self.rect.x <= -10:
            frag.remove(self)
        elif self.rect.x >= screenw+10:
            frag.remove(self)
def reset():
    lifes = 5
    player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
hullmyts = Player(screenw/2,screenh/2)
player.add(hullmyts)
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mup = True
            elif event.key == pg.K_DOWN:
                mdown = True
            elif event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                reset()
            elif event.key == pg.K_SPACE:
                tnt.add(TNT(hullmyts.getxy()[0], hullmyts.getxy()[1]))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        pd = "PAUSED"
        ptext = dfont.render(pd, True, (127,127,127))
        ptext_rect = ptext.get_rect()
        ptext_rect.centerx = screen.get_rect().centerx
        ptext_rect.y = 50
        screen.blit(ptext,ptext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    if lifes == 0:
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
        gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
    while r.uniform(0,1+(10/(lvl+1))) <= 1:
        stars.add(Star(r.randint(0,screenw), 1, redstar))
    while r.uniform(0,1+(10/(lvl+1))) <= 1:
        ystars.add(Star(r.randint(0,screenw), 1, yellowstar))
    scol = pg.sprite.spritecollide(hullmyts,stars,False)
    if len(scol) > 0:
        lifes -= 1
        stars.remove(scol)
    pcol = pg.sprite.spritecollide(hullmyts,ystars,False)
    if len(pcol) > 0:
        points += 1
        ystars.remove(pcol)
    tcol = pg.sprite.groupcollide(tnt, stars, True, True)
    if len(tcol.values()) > 0:
        for star in tcol.values():
            points += 1
            for x in range(r.randint(5,20)):
                frag.add(Frag(star[0].rect.x,star[0].rect.y,r.randint(-10,10),r.randint(-10,10)))
    fcol = pg.sprite.groupcollide(frag, stars, True, True)
    if len(tcol.values()) > 0:
        for star in tcol.values():
            points += 1
    ## increase distance and compute new level, speed
    distance += vel
    if distance > threshold:
        lvl += 1
        threshold = nextThreshold(distance, vel)
        vel = lvl+1
    ## update display
    screen.fill((0,0,0))
    score = ("Lifes: " + str(lifes) +
             " Points: " + str(points) +
             " Distance: " + str(distance) +
             " Level: " + str(lvl))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mup,mdown, mleft, mright)
    player.draw(screen)
    stars.update(vel)
    stars.draw(screen)
    ystars.update(vel)
    ystars.draw(screen)
    tnt.update()
    tnt.draw(screen)
    frag.update()
    frag.draw(screen)
    pg.display.update()
    ##
    timer.tick(60)

pg.quit()
