import pygame as pg
import time as t
import math as maths

class Box(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,x,y,lenx,leny,c,direction,num=0):
        self.x = x
        self.y = y

        self.lenx = lenx
        self.leny = leny

        self.colour = c

        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)

        self.dir = float(direction)

        self.num = num

        if c == (255,0,0):
            self.sort = 'basic'
        elif c == (255,0,255):
            self.sort = 'breakable'
    
    def update_rect(self):
        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)

class Player(): #this is the player
    def __init__(self,x,y,lenx,leny,c):
        self.x = x
        self.y = y

        self.lenx = lenx
        self.leny = leny/2

        self.dx = 0
        self.dy = 0

        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)
        self.state = 'air'
        self.dashspeed = 0.5
        self.dir = 0

        self.sort = 0
        self.set_att()
        self.movestyle = ''
        
    def update_rect(self): #This updates the position of the pygame object
        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)
    def set_att(self):
        att = {0:[(0,0,255), -0.7, 0.001, self.y+25, 25],
               1:[(0,255,0), -0.95, 0.001, self.y-25, 50],
               2:[(255,0,0), -0.7, 0.001, self.y, 50],
               3:[(255,255,0), -0.7, 0.001, self.y, 50]}
        self.colour = att[self.sort][0]
        self.jump = att[self.sort][1]
        self.fall = att[self.sort][2]
        self.y = att[self.sort][3]
        self.leny = att[self.sort][4]
        
    def transform(self):# this converts between bugs
        self.sort = (self.sort+1)%4
        self.set_att()
        self.state = 'air'
        self.has_dash = True

    def special(self):
        if self.sort == 2:
            p.state = 'glide'
        elif self.sort == 3 and self.has_dash:
            p.state='dash'
            #self.has_dash = False
    
def box_maker(x,y,lenx,leny, assets, colour, num=0): #Can be used to create a box, i.e. floor, ceiling, two walls, and filled in
    assets.append(Box(x,y+1,10,leny-2,colour,-90,num))
    assets.append(Box(x+lenx-10,y+1,10,leny-2,colour,-90,num))
    assets.append(Box(x+1,y,lenx-2,10,colour,180,num))
    assets.append(Box(x+1,y+leny-10,lenx-2,10,colour,180,num))
    assets.append(Box(x+1,y+1,lenx-2, leny-2,colour,180,num))
    return assets
    
    
#initialise pygame
pg.init()
screen = pg.display.set_mode((800,600))
clock = pg.time.Clock()
d = 0.3
dx = dy = 0

p = Player(375,200,50,50,(0,0,255))

assets = []
assets = box_maker(500,400,300,200,assets,(255,0,0))
assets = box_maker(0,200,200,330,assets,(255,0,0))

assets.append(Box(-800,570,1600,30,(255,0,0),180))
assets.append(Box(-800,0,1600,30,(255,0,0),180))
assets.append(Box(-800,0,30,600,(255,0,0),-90))
assets.append(Box(771,0,30,600,(255,0,0),-90))

assets = box_maker(0,530,200,40,assets,(255,0,255),1)
assets = box_maker(0,30,200,170,assets,(255,0,255),2)

assets_invis = []
assets_invis = box_maker(425,0,375,600,assets_invis,(255,0,255))
assets_invis = box_maker(-800,0,375,600,assets_invis,(255,0,255))

running = True
while running:
    screen.fill((0,0,0))
    pressed = pg.key.get_pressed()
    if pressed[pg.K_a] and p.dx > -d:
        p.dx -= d
        p.dir = -1
    if pressed[pg.K_d] and p.dx < d:
        p.dx += d
        p.dir = 1
    if (not pressed[pg.K_d]) and (not pressed[pg.K_a]):
        p.dx = 0
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: #quits game
                running = False
            elif event.key == pg.K_w and p.state == 'ground': #jump
                p.dy = p.jump
                p.state = 'air'
            elif event.key == pg.K_UP:
                p.special()
                if p.has_dash:
                    s = t.time()
                    p.has_dash=False
            elif event.key == pg.K_RETURN:
                p.transform()
                p.update_rect()
                colls = p.rect.collidelistall(assets)
                if len(colls) > 0:
                    p.sort = (p.sort-1)%4
                    p.set_att()
                    print('no space')
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP and p.sort == 2: #ladybird glide end
                p.state='air'
                p.fall = 0.001

    if p.state == 'dash' and t.time()-s < 0.3:
        p.dx = p.dashspeed*p.dir
        p.dy = 0
    elif p.state == 'dash' and t.time()-s > 0.3:
        p.state = 'air'
        p.dx = 0
        p.dy = 0
    elif p.state == 'glide':
        p.fall = 0
        p.dy = 0.1
    else:
        p.state='air'
    p.dy += p.fall #gravity

    p.y += p.dy
    p.x += p.dx
    p.update_rect()

    if len(p.rect.collidelistall(assets_invis))==0:
        p.movestyle = 'scroll'
        p.x -= p.dx
        for ob in assets:
            ob.x -= p.dx
            ob.update_rect()
        for ob in assets_invis:
            ob.x -= p.dx
            ob.update_rect()
    else:
        p.movestyle = 'static'

    p.update_rect()
    
    colls = [True]
    while len(colls) > 0: #detect and resolve collisions
        colls = p.rect.collidelistall(assets)
        for i in colls:
            ob = assets[i]
            x = p.dx*maths.sin(ob.dir*maths.pi/180)
            p.y += p.dy*maths.cos(ob.dir*maths.pi/180)
            if ob.dir == float(180) and p.state != 'dash':
                p.state = 'ground'
                p.dy = 0
                p.has_dash = True
            if ob.sort == 'breakable' and p.state == 'dash':
                rem = [ob2 for ob2 in assets if ob2.num == ob.num]
                for i in rem:
                    assets.remove(i)
                p.state = 'air'
                p.dx = 0
                p.dy = 0
            p.update_rect()
            if p.movestyle=='scroll':
                for ob2 in assets:
                    ob2.x -= x
                    ob2.update_rect()
                for ob2 in assets_invis:
                    ob2.x -= x
                    ob2.update_rect()
            else:
                p.x += x
    pg.draw.rect(screen, p.colour, p.rect)
    for ob in assets: #put objects on screen
        pg.draw.rect(screen, ob.colour, ob.rect)
    #for ob in assets_invis: #put objects on screen
    #    pg.draw.rect(screen, ob.colour, ob.rect)
    pg.display.update()
