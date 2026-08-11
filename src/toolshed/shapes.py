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

class Rect: 
    def __init__(self, x, y, w, h, col=(0,0,0)):
            self.x = x 
            self.y = y 
            self.w = w 
            self.h = h
            self.col = col

    def to_pygame_rect(self): 
        return pg.Rect(self.x, self.y, self.w, self.h)  
    
    def pos(self): 
        return self.x, self.y 
    
    def center(self): 
        return self.x + self.w // 2, self.y + self.h // 2

    def draw(self, surf: pg.Surface): 
        pg.draw.rect(surf, self.col, self.to_pygame_rect())  

    def draw_outline(self, surf: pg.Surface, color: tuple[int, int, int] = None): 
        c = color if color is not None else self.col
        pg.draw.rect(surf, c, pg.Rect(self.x, self.y, self.w, self.h), width=1) 

    # Rect 'a' is the rect that is movable 
    # Rect 'other' is passed as an arg and is immovable
    def collide(self, other: Rect, adjust_x: bool, adjust_y: bool): 
        if not isinstance(other, Rect): 
            return False
        
        xa1, xa2 = self.x, self.x + self.w
        ya1, ya2 = self.y, self.y + self.h
        xb1, xb2 = other.x, other.x + other.w
        yb1, yb2 = other.y, other.y + other.h
        colliding_x = not (xa1 >= xb2 or xa2 <= xb1)
        colliding_y = not (ya1 >= yb2 or ya2 <= yb1)

        if not (colliding_x and colliding_y): 
            return False
        
        movable_center = self.center()
        immovable_center = other.center()

        # adjust x 
        if adjust_x: 
            self.x = xb2 if movable_center[0] > immovable_center[0] else xb1 - other.w 
        
        # adjust y 
        if adjust_y: 
            self.y = yb2 if movable_center[1] > immovable_center[1] else yb1 - other.h 

        return True 