import pygame as pg
import time as t

class Box(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,x,y,lenx,leny,c,direction):
        self.x = x
        self.y = y

        self.lenx = lenx
        self.leny = leny

        self.colour = c

        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)

        self.dir = direction

class Player(): #this is the player
    def __init__(self,x,y,lenx,leny,c):
        self.x = x
        self.y = y

        self.lenx = lenx
        self.leny = leny

        self.dx = 0
        self.dy = 0

        self.colour = c

        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)

        self.state = 'air'

        self.jump = -0.7
        self.fall = 0.001

        self.sort = 0
        
    def refresh_rect(self): #This updates the position of the pygame object
        self.rect = pg.Rect(self.x, self.y, self.lenx, self.leny)

    def transform(self):# this converts between bugs
        if self.sort == 0: #ant -> grasshopper
            self.colour = (0,255,0)
            self.jump = -0.95
        elif self.sort == 1: #grasshopper -> ladybird
            self.colour = (255,0,0)
            self.jump = -0.7
        elif self.sort == 2: #ladybird -> ant
            self.colour = (0,0,255)
            self.fall = 0.001
        self.sort = (self.sort+1)%3
    
def box_maker(x,y,lenx,leny, assets): #Can be used to create a box, i.e. floor, ceiling, two walls, and filled in
    assets.append(Box(x,y+1,10,leny-2,(255,0,0),'v'))
    assets.append(Box(x+lenx-10,y+1,10,leny-2,(255,0,0),'v'))
    assets.append(Box(x+1,y,lenx-2,10,(255,0,0),'h'))
    assets.append(Box(x+1,y+leny-10,lenx-2,10,(255,0,0),'h'))
    assets.append(Box(x+1,y+1,lenx-2, leny-2,(255,0,0),'h'))
    return assets
    
    
#initialise pygame
pg.init()
screen = pg.display.set_mode((800,600))
d = 0.3
dx = dy = 0

p = Player(200,200,50,50,(0,0,255))

assets = box_maker(500,400,300,200,[])
assets = box_maker(0,200,200,400,assets)
assets.append(Box(0,570,800,30,(255,0,0),'h'))
assets.append(Box(0,0,800,30,(255,0,0),'h'))

running = True
while running:
    screen.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: #quits game
                running = False
            elif event.key == pg.K_UP and p.state == 'ground': #jump
                p.dy = p.jump
                p.state = 'air'
            elif event.key == pg.K_LEFT:
                p.dx -= d
            elif event.key == pg.K_RIGHT:
                p.dx += d
            elif event.key == pg.K_SPACE and p.sort == 2: #convert to next bug
                p.dy = 0.1
                p.fall = 0
            elif event.key == pg.K_RETURN:
                p.transform()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                p.dx += d
            elif event.key == pg.K_RIGHT:
                p.dx -= d
            elif event.key == pg.K_SPACE and p.sort == 2: #ladybird glide
                p.fall = 0.001          
    p.state='air'
    p.dy += p.fall #gravity
    p.x = min(max(p.x+p.dx,0),800-p.lenx)
    p.y += p.dy
    #print(p.fall, p.dy)
    p.refresh_rect()

    colls = [True]
    c = 0
    while len(colls) > 0: #detect and resolve collisions
        c += 1
        colls = p.rect.collidelistall(assets)
        for i in colls:
            ob = assets[i]
            if ob.dir == 'v':
                p.x -= p.dx
            elif ob.dir == 'h':
                p.y -= p.dy
                p.dy = 0
                p.state = 'ground'
            p.refresh_rect()
        if c == 10: #used in case it gets stuck in a corner, made for floors so might fail with ceilings/walls
            c = 0
            p.y -= 2
            p.x -= 2
            p.refresh_rect()
    pg.draw.rect(screen, p.colour, p.rect)
    for ob in assets: #put objects on screen
        pg.draw.rect(screen, ob.colour, ob.rect)
    pg.display.update()
