import pygame as pg 

class AtlasManager: 
    def __init__(self, sprite_sheet: pg.Surface, offsets): 
        self.sprite_sheet = sprite_sheet
        self.offsets = offsets 

    def sprite(self, id): 
        return self.sprite_sheet.subsurface(self.offsets[id])