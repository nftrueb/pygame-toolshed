import asyncio
from pathlib import Path

import pygame as pg

from toolshed import get_logger, PICO_COLORS
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.gif import capture_screenshot, GifManager
from toolshed.easing import EaseManager
import toolshed.reload as reload

import demo.external as e
import demo.configs as c

logger = get_logger()

class App: 
    def __init__(self): 
        self.pc = PygameContext((c.WIDTH, c.HEIGHT), 'Demo Project', icon_path='./assets/icon.png')
        self.pm = ParticleManager()
        self.em = EaseManager()
        self.gm = GifManager()
        self.printer = 'regular'
        self.reloader = reload.Reloader(Path(__file__).absolute().parent, 'demo')
        self.running = True
        self.config = c.Config

    async def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
                self.update()
                self.reloader.try_reloading()
                await asyncio.sleep(0)
        except (asyncio.CancelledError, KeyboardInterrupt): 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 
        finally: 
            pg.quit() 
        logger.info('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill(PICO_COLORS.White.value)
        c.printers[self.printer].print_center(self.pc.frame, e.get_version(), (c.WIDTH//2, c.HEIGHT//2))
        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()
        self.gm.record(self.pc.frame)

    def update(self): 
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
