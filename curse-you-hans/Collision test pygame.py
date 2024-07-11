import pygame as pg
import time as t
import math as maths
import numpy as np

def sum_val(lis1,lis2): #these two are used to add/subtract lists together such that [a,b] + [c,d] = [a+c,b+d]. Yes i know i can do this in python but I cba to find out.
    return [a+b for a,b in zip(lis1,lis2)]

def minus_val(lis1,lis2):
    return [a-b for a,b in zip(lis1,lis2)]

class Box(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,pos,c,sort='basic'):
        self.pos = [pos[0],pos[2]]
        self.lens = [pos[1]-pos[0],pos[3]-pos[2]]
        self.colour = c
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #this rectange object is a pygame object so it's the bit that's pasted to the screen
        self.sort = sort
    
    def update_rect(self):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.

class Player(): #this is the player
    def __init__(self,pos,lens,c):
        self.pos = pos #position
        self.velo = [0,0] #speed
        self.accel = [0,0] #acceleration

        self.lens = lens #lens = lengths

        self.dir = 0 #direction
        self.dashspeed = 10 #speed of dash
        self.fall = 0.5 #speed of falling
        self.jump = 15 #speed of jump
        self.glide = 1 #speed of falling while gliding

        self.sort = 0 #what mode is the player in
        self.set_att() #each mode has a set of attributes (see set_att())
        self.movestyle = '' #movestyle denotes whether the screen is scrolling or static (see movement)
        self.has_dash = True #player regains dash when hitting ground
        self.dash_f = 0 #counts the frames so it knowns when to kill dash
        self.lives = [3,0] #first is the number of lives, second is the change.
        self.invincible = False #losing a life grants you 80 frames of invincibility
        self.invinc_f = 0 #counts the frames until invincibility is over
        
        self.state = 'air' #is it in the air, on the ground, gliding, or dashing?
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #rectangle object again
        
    def update_rect(self): #This updates the position of the pygame object
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1])

    def set_att(self):
        att = {0:[(0,0,255), -15, self.pos[1]+25, 25],
               1:[(0,255,0), -22, self.pos[1]-25, 50],
               2:[(255,0,0), -15, self.pos[1], 50],
               3:[(255,255,0), -15, self.pos[1], 50]}
        self.colour = att[self.sort][0] #colour, different modes have different colours
        self.jump = att[self.sort][1] #jump height,
        self.pos[1] = att[self.sort][2] #character position, this is important as position is determined by top left corner, so altering height by just changing height will put the character in the floor or above the ground
        self.lens[1] = att[self.sort][3] # character height
        
    def transform(self):# this converts between modes
        self.sort = (self.sort+1)%4 #go to next mode
        self.set_att() #set correct attributes
        self.state = 'air' #set the state to air
        if self.sort == 3:
            self.has_dash = True #ensure dasher can dash

    def special(self): #these contain the special moves gliding and dashing
        if self.sort == 2:
            p.state = 'glide'
        elif self.sort == 3 and self.has_dash:
            p.state='dash'

    def test_scroll(self,assets_invis): #at the edges of the map I have shapes to determine whether the obsticales should scroll with the character or remain static.
        self.pos[0] += self.velo[0]
        self.update_rect()
        if len(p.rect.collidelistall(assets_invis)) > 0:
            self.movestyle = 'static'
        else:
            self.movestyle = 'scroll'
            self.pos[0] = 375
            self.update_rect()
    
    def move(self, assets, assets_invis):
        self.velo = sum_val(self.accel,self.velo) #update velocity by adding acceleration
        self.test_scroll(assets_invis) #find scroll or static
        if self.movestyle == 'static': #first I resolve x direction to check for collisions
            #since test_scroll already moves character in x direction, not necessery here
            assets = self.check_coll(self.movestyle,self.velo[0],assets,assets_invis)
        elif self.movestyle == 'scroll':#if the screen is scrolling all the background objects need to move
            for ob in assets:
                ob.pos[0] -= self.velo[0]
                ob.update_rect()
            for ob in assets_invis: #this includes the hidden ones to check if the screen should scroll or static
                ob.pos[0] -= self.velo[0]
                ob.update_rect()
            assets = self.check_coll(self.movestyle,-self.velo[0],assets,assets_invis)
        if self.state != 'dash': #now we resolve y direction, not necessery if dashing because it won't move down.
            self.pos[1] += self.velo[1] #update y position
            p.update_rect()
            assets = self.check_coll('y',self.velo[1],assets,assets_invis) #check for collision
        return assets
        
    def check_coll(self,kind,dis,assets,assets_invis): #kind tells you what sort of collision to do, y direction, scroll, or static, because each need a different effect.
        colls = p.rect.collidelistall(assets) #is there any overlap between the player and obstacles
        rem = []
        for i in colls: #if yes, cycles through the object indicies
            ob = assets[i] #converts indicie to object
            if kind == 'y': #y direction collision resolution
                self.state='ground'
                self.has_dash = True #if you hit the ground give dash and ground state to allow jump
                self.velo[1] = 0 #also y speed should be 0
                if dis > 0: # if you move down
                    self.pos[1] = ob.pos[1]-self.lens[1]+0.5 #snap to top of floor
                elif dis < 0: #if up
                    self.pos[1] = ob.pos[1]+ob.lens[1]+0.5 #to bottom of roof
            elif kind == 'static': #if the background is static
                self.velo[0] = 0 #make the player x speed 0
                if dis > 0: #and snap to left or right of wall.
                    self.pos[0] = ob.pos[0]-self.lens[0]
                    self.has_dash = True
                elif dis < 0:
                    self.pos[0] = ob.pos[0]+ob.lens[0]
            elif kind == 'scroll': #if the background is scrolling, snap the wall to the character.
                dx = 0
                self.velo[0] = 0
                if dis > 0:
                    dx = self.pos[0]-(ob.pos[0]+ob.lens[0])
                elif dis < 0:
                    dx = (self.pos[0]+self.lens[0])-ob.pos[0]
                for ob2 in assets:
                    ob2.pos[0] += dx
                    ob2.update_rect()
                for ob2 in assets_invis:
                    ob2.pos[0] += dx
                    ob2.update_rect()
            if ob.sort == 'breakable' and p.state == 'dash':
                rem.append(ob) #dashing can break breakable blocks, so record any broken blocks and remove them.
            if ob.sort == 'damage' and self.invincible == False:
                self.lives[1] = -1 #if the block has the damage property, deal damage.
        for ob in rem:
            assets.remove(ob) #remove broken blocks
        return assets
        
pg.init() #initialise pygame
screen = pg.display.set_mode((800,600)) #create screen
clock = pg.time.Clock()
d = 5 #how far to move left and right

p = Player([375,200],[50,25],(0,0,255)) #generate player

c_basic = (128,128,128) #set colours for obstacles
c_breakable = (150,75,0)
c_invis = (255,255,255)
c_lava = (255,102,0)

assets = [] #lrtb for coords
assets.append(Box([-800,1600,570,600],c_basic)) #create obstacles
assets.append(Box([-800,1600,0,30],c_basic))

assets.append(Box([-800,-770,0,600],c_basic))
assets.append(Box([1570,1600,0,600],c_basic))

assets.append(Box([0,200,200,530],c_basic))
assets.append(Box([500,800,400,600],c_basic))

assets.append(Box([0,200,30,200],c_breakable,'breakable')) #breakable ones get broken if dashed into
assets.append(Box([0,200,530,570],c_breakable,'breakable'))

assets.append(Box([800,1200,570,600],c_lava,'damage')) #lava ones damage

assets_invis = []
assets_invis.append(Box([1225,1600,0,600],c_invis))
assets_invis.append(Box([-800,-425,0,600],c_invis)) #invisible blockes at the edges tell it if the player or background should move

f_c = 0 #frame counter used to time dashes and invincibility after taking damage
print('Lives:',p.lives[0])
running = True
while running: #start game!
    #print(p.state)
    screen.fill((0,0,0)) #make the screen black
    pressed = pg.key.get_pressed()
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
    assets = p.move(assets, assets_invis) #move
    p.update_rect() #update player position
    
    for ob in assets_invis: #put invisible objects on screen for my reference
        pg.draw.rect(screen, ob.colour, ob.rect) #can be commented out to make them invisible
        pass
    
    if p.invincible == True and f_c-p.invinc_f > 80:
        p.invincible = False #once 80 frames since taking damage are over make not invincible
    if p.invincible == False:
        pg.draw.rect(screen, p.colour, p.rect) #if not invincible display player
    elif p.invincible == True and maths.floor((f_c-p.invinc_f)/8)%2 == 0:
        pg.draw.rect(screen, p.colour, p.rect) #if are invincible flash the player
    if p.lives[1] != 0: #if lives have changed, change the live counter and print to terminal
        p.lives = [p.lives[0]+p.lives[1],0]
        p.invincible = True #make invincible
        p.invinc_f = f_c #start counting i frames
        print('Lives:',p.lives[0]) #print lives
    if p.lives[0] == 0:
        running = False
        print('you died :(') #if lives have run out, the player is dead :(
    for ob in assets: #put objects on screen
        pg.draw.rect(screen, ob.colour, ob.rect)

    pg.display.update() #update screen
    clock.tick(60) #delay to keep game at 60 fps
    f_c += 1 #increase frame counter by 1
