import asyncio

import pygame as pg

from toolshed import get_logger, DEFAULT_PICO8_FONT_SIZE, PICO8_DIMS
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.ttf_printer import ShadowDirection, init_printers

WIDTH, HEIGHT = PICO8_DIMS

logger = get_logger()

printer_params = {
    'outline': {
        'font': {
            'filename': 'assets/PICO-8.ttf', 
            'size': DEFAULT_PICO8_FONT_SIZE
        },
        'color': (225, 225, 225),
        'shadow_color': (0,0,0), 
        'shadow_direction': ShadowDirection.Outline
    }, 
    'ui': {
        'font': {
            'filename': 'assets/PICO-8.ttf', 
            'size': DEFAULT_PICO8_FONT_SIZE
        },
        'color': (170, 170, 255),
        'shadow_color': (0,0,0), 
        'shadow_direction': ShadowDirection.Right 
    }
}

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Text Demo', icon_path='./assets/icon.png')
        self.pm = ParticleManager()
        self.running = True
        self.printers = init_printers(printer_params)
        self.debug = True

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
        self.pc.frame.fill((255,255,255))

        text = 'Hello World'
        self.printers['outline'].print_center(self.pc.frame, text, (WIDTH // 2, HEIGHT // 4))
        self.printers['outline'].print_center(self.pc.frame, text, (WIDTH//2, HEIGHT//2), color = (200, 255, 200))
        self.printers['ui'].print_center(self.pc.frame, text, (WIDTH//2, HEIGHT//4*3))
        
        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()

    def update(self): 
        self.pm.update()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False

                if event.key == pg.K_SPACE: 
                    self.debug = not self.debug

            elif event.type == pg.MOUSEBUTTONUP: 
                if event.button == pg.BUTTON_LEFT:
                    logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

def main(): 
    asyncio.run(App().run())

if __name__ == '__main__': 
    main()
