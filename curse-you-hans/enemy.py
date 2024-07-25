import pygame as pg
from functions import sum_val, minus_val

class Enemy():
    def __init__(self,pos,lens,colour):
        self.pos = pos
        self.disp_pos = [pos[0],pos[1]]
        self.lens = lens
        self.colour = colour
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1])
        self.velo = [3,0]
        
    def update_rect(self): #This updates the position of the pygame object
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.lens[0], self.lens[1])

    def update_disp_rect(self): #This updates the position of the pygame object
        self.disp_rect = pg.Rect(self.disp_pos[0], self.disp_pos[1], self.lens[0], self.lens[1])

    def move(self,assets):
        self.pos = sum_val(self.pos,self.velo)
        self.collision(assets)
        self.update_rect()

    def collision(self,assets):
        colls = self.rect.collidelistall(assets)
        for i in colls:
            ob = assets[i]
            if self.velo[0] > 0:
                self.pos[0] = ob.pos[0]-self.lens[0]
                self.velo[0] *= -1
                return
            else:
                self.pos[0] = ob.pos[0]+ob.lens[0]
                self.velo[0] *= -1
                return
