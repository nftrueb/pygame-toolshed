from pathlib import Path
from dataclasses import dataclass
from typing import Tuple 
from enum import Enum, auto

import pygame as pg

from toolshed import get_logger
from toolshed.window import PygameContext

WIDTH, HEIGHT = 320, 180

logger = get_logger()

# LIBRARY 
class AtlasManager:
    def __init__(self, sprite_sheet: pg.Surface, offsets): 
        self.sprite_sheet = sprite_sheet 
        self.offsets = offsets

    def get_sprite(self, sprite_name) -> pg.Surface: 
        return self.sprite_sheet.subsurface(self.offsets[sprite_name]) 

    
# APP UTILS
class ASN(Enum): 
    ChestClosed = auto()
    ChestOpened = auto()

atlas_offset = {
    ASN.ChestClosed: (96, 0, 16, 16), 
    ASN.ChestOpened: (112,0, 16, 16)
}

am = AtlasManager(pg.image.load('assets/assets.png'), atlas_offset)

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT))
        self.running = True

    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
        except KeyboardInterrupt: 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((255,255,255))
        self.pc.frame.blit(am.get_sprite(ASN.ChestClosed), (0,0))
        self.pc.frame.blit(am.get_sprite(ASN.ChestOpened), self.pc.get_event_context().mouse_pos)

        self.pc.finish_drawing_frame()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

            elif event.type == pg.MOUSEBUTTONUP: 
                logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()