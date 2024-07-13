import pygame as pg

class Box(): #creates an object, eg. wall, floor, ceiling
    def __init__(self,pos,c,sort='basic'):
        self.pos = [pos[0],pos[2]]
        self.lens = [pos[1]-pos[0],pos[3]-pos[2]]
        self.colour = c
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #this rectange object is a pygame object so it's the bit that's pasted to the screen
        self.sort = sort
    
    def update_rect(self):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1]) #if the box moves the rectangle needs to be updated to the new coords.
