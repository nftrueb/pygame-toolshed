import pygame as pg 

class AtlasManager: 
    def __init__(self, offsets): 
        self.sprite_sheet: pg.Surface | None = None
        self.offsets = offsets 

    def sprite(self, id): 
        return self.sprite_sheet.subsurface(self.offsets[id])