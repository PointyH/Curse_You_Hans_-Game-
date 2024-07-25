import pygame as pg

class Box(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,pos,c,breakable=False,damage=False):
        self.pos = [pos[0],pos[2]]
        self.disp_pos = [pos[0],pos[2]]
        self.lens = [pos[1]-pos[0],pos[3]-pos[2]]
        self.colour = c
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #this rectange object is a pygame object so it's the bit that's pasted to the screen
        self.breakable = breakable
        self.damage = damage
    
    def update_rect(self):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.
        return

    def update_disp_rect(self):
        self.disp_rect = pg.Rect(self.disp_pos[0], self.disp_pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.
        return

class Edge(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,pos,c,direction):
        self.pos = [pos[0],pos[2]]
        self.disp_pos = [pos[0],pos[2]]
        self.lens = [pos[1]-pos[0],pos[3]-pos[2]]
        self.colour = c
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #this rectange object is a pygame object so it's the bit that's pasted to the screen
        self.dir = direction
        
    def update_rect(self):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.
        return

    def update_disp_rect(self):
        self.disp_rect = pg.Rect(self.disp_pos[0], self.disp_pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.
        return
