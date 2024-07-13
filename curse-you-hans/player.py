import pygame as pg
from list_mod import sum_val, minus_val

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
        return
        
    def update_rect(self): #This updates the position of the pygame object
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1])
        return

    def set_att(self):
        att = {0:[(0,0,255), -15, self.pos[1]+25, 25],
               1:[(0,255,0), -22, self.pos[1]-25, 50],
               2:[(255,0,0), -15, self.pos[1], 50],
               3:[(255,255,0), -15, self.pos[1], 50]}
        self.colour = att[self.sort][0] #colour, different modes have different colours
        self.jump = att[self.sort][1] #jump height,
        self.pos[1] = att[self.sort][2] #character position, this is important as position is determined by top left corner, so altering height by just changing height will put the character in the floor or above the ground
        self.lens[1] = att[self.sort][3] # character height
        return
        
    def transform(self):# this converts between modes
        self.sort = (self.sort+1)%4 #go to next mode
        self.set_att() #set correct attributes
        self.state = 'air' #set the state to air
        if self.sort == 3:
            self.has_dash = True #ensure dasher can dash
        return

    def special(self): #these contain the special moves gliding and dashing
        if self.sort == 2:
            self.state = 'glide'
        elif self.sort == 3 and self.has_dash:
            self.state='dash'
        return

    def test_scroll(self,assets_invis): #at the edges of the map I have shapes to determine whether the obsticales should scroll with the character or remain static.
        self.pos[0] += self.velo[0]
        self.update_rect()
        if len(self.rect.collidelistall(assets_invis)) > 0:
            self.movestyle = 'static'
        else:
            self.movestyle = 'scroll'
            self.pos[0] = 375
            self.update_rect()
        return
    
    def move(self,assets,enemies,assets_invis):
        self.velo = sum_val(self.accel,self.velo) #update velocity by adding acceleration
        self.test_scroll(assets_invis) #find scroll or static
        if self.movestyle == 'static': #first I resolve x direction to check for collisions
            #since test_scroll already moves character in x direction, not necessery here
            assets,enemies,assets_invis = self.check_coll(self.movestyle,self.velo[0],assets,enemies,assets_invis)
        elif self.movestyle == 'scroll':#if the screen is scrolling all the background objects need to move
            for ob in assets:
                ob.pos[0] -= self.velo[0]
                ob.update_rect()
            for ob in enemies: #this includes the hidden ones to check if the screen should scroll or static
                ob.pos[0] -= self.velo[0]
                ob.update_rect()
            for ob in assets_invis: #this includes the hidden ones to check if the screen should scroll or static
                ob.pos[0] -= self.velo[0]
                ob.update_rect()
            assets,enemies,assets_invis = self.check_coll(self.movestyle,-self.velo[0],assets,enemies,assets_invis)
        if self.state != 'dash': #now we resolve y direction, not necessery if dashing because it won't move down.
            self.pos[1] += self.velo[1] #update y position
            self.update_rect()
            assets,enemies,assets_invis = self.check_coll('y',self.velo[1],assets,enemies,assets_invis) #check for collision
        if not self.invincible:
            self.check_enemy(enemies)
        return assets,enemies,assets_invis
        
    def check_coll(self,kind,dis,assets,enemies,assets_invis): #kind tells you what sort of collision to do, y direction, scroll, or static, because each need a different effect.
        colls = self.rect.collidelistall(assets) #is there any overlap between the player and obstacles
        rem = []
        kill_dash = False
        for i in colls: #if yes, cycles through the object indicies
            kill_dash = True
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
                for ob2 in enemies:
                    ob2.pos[0] += dx
                    ob2.update_rect()
            if ob.sort == 'breakable' and self.state == 'dash':
                rem.append(ob) #dashing can break breakable blocks, so record any broken blocks and remove them.
            if ob.sort == 'damage' and not self.invincible:
                self.lives[1] = -1 #if the block has the damage property, deal damage.
                self.invincible = True
        for ob in rem:
            assets.remove(ob) #remove broken blocks
        if self.state == 'dash' and kill_dash: #if you hit a wall while dashing cancel the dash
            self.state = 'air' #this can't be done in the loop as the dash can get cancelled before a breakable block collision is resolved.
        return assets,enemies,assets_invis

    def check_enemy(self,enemies):
        colls = self.rect.collidelistall(enemies) #is there any overlap between the player and obstacles
        for i in colls: #if yes, cycles through the object indicies
            ob = enemies[i]
            self.lives[1] = -1
            self.invincible = True
        return
