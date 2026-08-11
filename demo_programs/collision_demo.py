import asyncio
from enum import StrEnum, auto
from dataclasses import dataclass 
from typing import Optional 

import pygame as pg

from toolshed import get_logger, PICO_COLORS
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.gif import capture_screenshot, GifManager
from toolshed.ttf_printer import Printer, init_printers
from toolshed.easing import EaseManager
from toolshed.shapes import Rect

from .configs import *

logger = get_logger()

class Dir(StrEnum): 
    Left = auto()
    Right = auto() 
    Up = auto() 
    Down = auto() 

    def is_horiz(self): 
        return self in HORIZONTAL_DIRS 
    
    def is_vert(self): 
        return self in VERTICAL_DIRS

@dataclass
class DirUpdate:
    dir: Optional[Dir]
    pos_offset: tuple[int, int] 

HORIZONTAL_DIRS = { Dir.Left, Dir.Right }
VERTICAL_DIRS = { Dir.Up, Dir.Down }
NO_DIR_UPDATE = DirUpdate(None, (0, 0))
    
def get_dir_update_horizontal(keys): 
    if keys[pg.K_LEFT]: 
        return DirUpdate(Dir.Left, (-1, 0))

    elif keys[pg.K_RIGHT]: 
        return DirUpdate(Dir.Right, (1, 0))
    
    return NO_DIR_UPDATE

def get_dir_update_vertical(keys): 
    if keys[pg.K_UP]: 
        return DirUpdate(Dir.Up, (0, -1))

    elif keys[pg.K_DOWN]: 
        return DirUpdate(Dir.Down, (0, 1))
    
    return NO_DIR_UPDATE

def get_dir_update_for_curr_frame(curr_dir: Dir, keys): 
    # if horizontal dir is already pressed from previous frame, only accept update in horizontal axis
    if curr_dir is not None: 
        if curr_dir.is_horiz():
            return get_dir_update_horizontal(keys)
        
        # same with vertical 
        elif curr_dir.is_vert(): 
            return get_dir_update_vertical(keys)

    # if no previous dir was selected, accept any direction update
    dir_update = get_dir_update_horizontal(keys)
    if dir_update != NO_DIR_UPDATE: 
        return dir_update 
    
    return get_dir_update_vertical(keys)
    
class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Collision Demo', icon_path='./assets/icon.png')
        self.pm = ParticleManager()
        self.em = EaseManager()
        self.gm = GifManager()
        self.printer: Printer = init_printers(printer_params)['regular']
        self.running = True

        self.rect1 = Rect(10, 10, 10, 10, PICO_COLORS.DarkBlue.value)
        self.rect2 = Rect(50, 50, 10, 10, PICO_COLORS.DarkBlue.value)
        self.colliding = False 
        self.dir = None 

    async def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
                self.update()
                await asyncio.sleep(0)
        except (asyncio.CancelledError, KeyboardInterrupt): 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 
        finally: 
            pg.quit() 
        logger.info('Successfully exited program ...') 

    def draw(self): 
        if self.colliding: 
            self.pc.frame.fill(PICO_COLORS.Red.value)
        else: 
            self.pc.frame.fill(PICO_COLORS.White.value)
        
        self.rect1.draw(self.pc.frame)
        self.rect2.draw(self.pc.frame)

        pg.draw.circle(self.pc.frame, (0,0,0), (self.rect1.x + self.rect1.w // 2, self.rect1.y + self.rect1.h // 2), 1)
        pg.draw.circle(self.pc.frame, (0,0,0), (self.rect2.x + self.rect2.w // 2, self.rect2.y + self.rect2.h // 2), 1)

        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()
        self.gm.record(self.pc.frame)

    def update(self):  
        self.colliding = False
        keys = pg.key.get_pressed()
        dir_update: DirUpdate = get_dir_update_for_curr_frame(self.dir, keys)
        self.dir = dir_update.dir 
        self.rect1.x += dir_update.pos_offset[0]
        self.rect1.y += dir_update.pos_offset[1]
        
        # if moving this frame, check for collision
        if self.dir is not None: 
            self.colliding = self.rect1.collide(self.rect2, self.dir.is_horiz(), self.dir.is_vert())

        self.em.update()
        self.pm.update()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False

                elif event.key == pg.K_s: 
                    capture_screenshot(self.pc.frame)

                elif event.key == pg.K_r: 
                    self.gm.toggle()
                    if not self.gm.toggle: 
                        self.gm.save()

            elif event.type == pg.MOUSEBUTTONUP: 
                if event.button == pg.BUTTON_LEFT:
                    logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

def main(): 
    asyncio.run(App().run())

if __name__ == '__main__': 
    main()
