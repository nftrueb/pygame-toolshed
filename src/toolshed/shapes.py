import pygame as pg 

class Circle: 
    def __init__(self, x, y, rad, col):
            self.x = x 
            self.y = y 
            self.rad = rad
            self.col = col  

    def draw(self, surf: pg.Surface): 
        pg.draw.circle(surf, self.col, (self.x, self.y), self.rad)  