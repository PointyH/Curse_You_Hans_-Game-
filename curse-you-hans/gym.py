import pygame as pg
#import time as t
import math as maths

from box import Box, Edge 
from player import Player
from enemy import Enemy

from functions import sum_val, minus_val

def render_room(room):
    assets = []
    assets_invis = []
    enemies = []
    edges = []
    
    for att in room['assets']:
        assets.append(Box(att[0],att[1],att[2],att[3]))
    for att in room['edges']:
        e = Edge(att[0],att[1],att[2])
        assets_invis.append(e)
        edges.append(e)
    for att in room['enemies']:
        enemies.append(Enemy(att[0],att[1],att[2]))
    player = Player(room['player'][0],room['player'][1],room['player'][2])
    boundary = room['boundary']
    return assets,assets_invis,enemies,player,boundary

pg.init() #initialise pygame
screen = pg.display.set_mode((800,600)) #create screen
clock = pg.time.Clock()
d = 5 #how far to move left and right

p = Player([375,200],[50,25],(0,0,255)) #generate player

c_basic = (128,128,128) #set colours for obstacles
c_breakable = (150,75,0)
c_invis = (255,255,255)
c_lava = (255,102,0)
c_enemy = (0,255,255)

room1 = {'assets': [[[-800,1600,570,600],c_basic,False,False], #lrtb for coords
                    [[-800,1600,-600,-570],c_basic,False,False],
                    [[-800,-770,-600,600],c_basic,False,False],
                    [[1570,1600,-600,600],c_basic,False,False],
                    [[0,200,200,530],c_basic,False,False],
                    [[500,800,400,600],c_basic,False,False],
                    [[0,200,30,200],c_breakable,True,False],
                    [[0,200,530,570],c_breakable,True,False],
                    [[800,1200,570,600],c_lava,False,True]],
         'edges': [[[-800,-800,-600,600],c_invis,'x'],
                   [[1600,1600,-600,600],c_invis,'x'],
                   [[-800,1600,-600,-600],c_invis,'y'],
                   [[-800,1600,600,600],c_invis,'y']],
         'enemies': [[[-450,545],[50,25],c_enemy]],
         'player': [[375,200],[50,25],(0,0,255)],
         'boundary':[-800,1600,-600,600]}

assets,assets_invis,enemies,player,boundary = render_room(room1)

f_c = 0 #frame counter used to time dashes and invincibility after taking damage
print('Lives:',p.lives[0])
running = True
while running: #start game!
    screen.fill((0,0,0)) #make the screen black
    pressed = pg.key.get_pressed()
    if p.state != 'dash':
        if pressed[pg.K_a] and p.velo[0] > -d: #if a or d is pressed move left or right
            p.velo[0] -= d
            p.dir = -1 #direction tells you which way to dash even if you aren't currently moving in a direction
        if pressed[pg.K_d] and p.velo[0] < d:
            p.velo[0] += d
            p.dir = 1
        if (not pressed[pg.K_d]) and (not pressed[pg.K_a]) and p.state != 'dash':
            p.velo[0] = 0 #make sure if neither direction is pressed you aren't moving
    if pressed[pg.K_UP] and p.sort == 2:
        p.state = 'glide' #if up arrow key and player is in gliding mode, glide because that's the glide button.
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN: #when you click a key
            if event.key == pg.K_ESCAPE: #quits game, without this pygame freezes
                running = False
            elif event.key == pg.K_w and p.state == 'ground': #jump
                p.velo[1] = p.jump
                p.state = 'air'
            elif event.key == pg.K_UP: #initiate special moves, aka, glide or dash
                p.special()
                if p.has_dash:
                    p.dash_f = f_c #set the dash frame counter to the current frame to check when dash is over.
                    p.has_dash=False #once you dash you need to touch the ground to do it again
            elif event.key == pg.K_RETURN: #enter changes mode
                p.transform()
                p.update_rect() #blue is small so rectangle object needs to be updated
                colls = p.rect.collidelistall(assets) #if changing mode creates a collision, go back.
                if len(colls) > 0:
                    p.sort = (p.sort-1)%4
                    p.set_att()
                    print('no space')
        elif event.type == pg.KEYUP: #when the key goes back up
            if event.key == pg.K_UP and p.sort == 2: #ladybird glide end
                p.state='air'
                p.accel = [0,0.2] #when gliding is done, return gravity to normal
    
    if p.state == 'dash' and f_c-p.dash_f < 20: #if dash is going, move like a dash
        p.velo = [p.dashspeed*p.dir,0]
    elif p.state == 'dash' and f_c-p.dash_f >= 20: #if 20 frames are over, cancel the dash
        p.state = 'air'
        p.velo = [0,0]
    elif p.state == 'glide': #if you glide don't accelerate towards the ground
        p.accel[1] = 0
        p.velo[1] = 1
    else: #if you fall off an object without jumping you don't want to jump, that's what this does.
        p.state = 'air'
    p.accel[1] = p.fall

    for e in enemies:
        e.move(assets)

    assets,enemies,assets_invis = p.move(assets,enemies,assets_invis) #move
    locx = 375
    locy = 400
    scroll = [abs(boundary[0]-(p.pos[0]+25)),
              abs(boundary[1]-(p.pos[0]+25)),
              abs(boundary[2]-(p.pos[1]+p.lens[1]-100)),
              abs(boundary[3]-(p.pos[1]+p.lens[1]-100))]

    if scroll[0] < 400:
        locx -= (400-scroll[0])
    elif scroll[1] < 400:
        locx += (400-scroll[1])
    if scroll[2] < 300:
        locy -= (300-scroll[2])
    elif scroll[3] < 300:
        locy += (300-scroll[3])
    p.scroll_screen(assets,assets_invis,enemies,locx,locy)

    for ob in assets_invis: #put invisible objects on screen for my reference
        pg.draw.rect(screen,ob.colour,ob.disp_rect) #can be commented out to make them invisible
        pass
    if p.lives[1] != 0: #if lives have changed, change the live counter and print to terminal
        p.lives = [p.lives[0]+p.lives[1],0]
        p.invinc_f = f_c #start counting i frames
        print('Lives:',p.lives[0]) #print lives
    elif p.invincible and f_c-p.invinc_f >= 80:
        p.invincible = False #once 80 frames since taking damage are over make not invincible
        
    if not p.invincible:
        pg.draw.rect(screen,p.colour,p.disp_rect) #if not invincible display player
    elif p.invincible and maths.floor((f_c-p.invinc_f)/8)%2 == 0:
        pg.draw.rect(screen,p.colour,p.disp_rect) #if are invincible flash the player

    if p.lives[0] == 0:
        running = False
        print('you died :(') #if lives have run out, the player is dead :(
    for ob in assets: #put objects on screen
        pg.draw.rect(screen,ob.colour,ob.disp_rect)
    for e in enemies:
        pg.draw.rect(screen,e.colour,e.disp_rect)

    pg.display.update() #update screen
    clock.tick(60) #delay to keep game at 60 fps
    #print(p.invincible)
    f_c += 1 #increase frame counter by 1
