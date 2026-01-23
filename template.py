import asyncio

import pygame as pg

from toolshed import get_logger
from toolshed.window import PygameContext

WIDTH, HEIGHT = 320, 180

logger = get_logger()

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Pygbag Template')
        self.running = True

    async def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
                await asyncio.sleep(0)
        except KeyboardInterrupt: 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((255,255,255))
        pg.draw.rect(self.pc.frame, (0,0,255), pg.Rect(50,50,50,50))
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

if __name__ == '__main__': 
    asyncio.run(App().run())
