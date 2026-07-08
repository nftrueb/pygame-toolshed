import pygame as pg 

class Circle: 
    def __init__(self, x, y, rad, col):
            self.x = x 
            self.y = y 
            self.rad = rad
            self.col = col  

    def draw(self, surf: pg.Surface): 
        pg.draw.circle(surf, self.col, (self.x, self.y), self.rad)  

    def draw_outline(self, surf: pg.Surface, color: tuple[int, int, int] = None): 
        c = color if color is not None else self.col
        pg.draw.circle(surf, c, (self.x, self.y), self.rad, width=1)