import asyncio

import pygame as pg

from toolshed import get_logger
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.mouse import Mouse, toggle_mouse_trail

WIDTH, HEIGHT = 320, 180

logger = get_logger()

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Template - Change this Title')
        self.pm = ParticleManager()
        self.running = True

        self.mouse = Mouse(
            rad=3, 
            outline_color=(50,50,50), 
            fill_color=(200,200,200), 
            particles_color=(200,200,200),
            click_particles=True, 
            mouse_pressed_event_handler=toggle_mouse_trail
        )
        self.mouse.init()

    async def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
                self.update()
                await asyncio.sleep(0)
        except KeyboardInterrupt: 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((255,255,255))
        self.pm.draw(self.pc.frame)
        self.mouse.draw(self.pc.frame)
        self.pc.finish_drawing_frame()

    def update(self): 
        self.mouse.update(self.pc)
        self.pm.update()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            self.mouse.handle_event(event, self.pm)
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

            elif event.type == pg.MOUSEBUTTONUP: 
                logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

if __name__ == '__main__': 
    asyncio.run(App().run())
