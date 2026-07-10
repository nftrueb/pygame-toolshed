import asyncio

import pygame as pg

from toolshed import get_logger, PICO_COLORS, PICO8_DIMS
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.gif import capture_screenshot, GifManager
from toolshed.shapes import Circle, Rect
from toolshed.ttf_printer import Printer, init_printers
from toolshed.easing import EaseManager, Ease, ease_in_out_cubic

from .configs import printer_params

logger = get_logger()

WIDTH, HEIGHT = PICO8_DIMS

MIN_RAD, MAX_RAD = 10, 40
X, Y, W, H = WIDTH//2 - 50, 5, 100, 30

MAX_W = WIDTH-2

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Demo Project', icon_path='./assets/icon.png')
        self.pm = ParticleManager()
        self.em = EaseManager()
        self.gm = GifManager()
        self.running = True
        self.debug = True
        self.printer: Printer = init_printers(printer_params)['regular']

        self.slide = 0 
        self.total_slides = 3

        self.circle = Circle(WIDTH // 2, HEIGHT // 2, MIN_RAD, PICO_COLORS.DarkBlue.value)
        self.growing = True 

        self.rect = Rect(X, Y, W, H, PICO_COLORS.DarkBlue.value)
        self.closing = True

        self.rect2 = Rect(1, 1, 10, 10, PICO_COLORS.DarkBlue.value)
        self.growing2 = True 

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
        self.pc.frame.fill(PICO_COLORS.White.value)

        if self.slide == 0: 
            self.draw_slide_0()
        elif self.slide == 1: 
            self.draw_slide_1()
        elif self.slide == 2: 
            self.draw_slide_2()

        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()
        self.gm.record(self.pc.frame)

    def draw_slide_0(self): 
        self.circle.draw(self.pc.frame)

    def draw_slide_1(self): 
        self.rect.draw(self.pc.frame)
        self.printer.print_center(self.pc.frame, 'Hello World', (self.rect.x + W//2, self.rect.y + H//2))

    def draw_slide_2(self): 
        self.rect2.draw(self.pc.frame)

    def update(self): 
        self.em.update()
        
        if self.slide == 0: 
            self.update_slide_0()
        elif self.slide == 1: 
            self.update_slide_1()
        elif self.slide == 2: 
            self.update_slide_2()

        self.pm.update()

    def update_slide_0(self): 
        ease: Ease = self.em.get('rad')
        if ease is not None: 
            self.circle.rad = ease.get()

    def update_slide_1(self): 
        pos_ease: Ease = self.em.get('pos')
        if pos_ease is not None: 
            self.rect.y = pos_ease.get()

    def update_slide_2(self): 
        ease: Ease = self.em.get('w')
        if ease is not None: 
            self.rect2.w = ease.get()
            self.rect2.h = self.rect2.w

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False

                elif event.key == pg.K_SPACE: 
                    if self.slide == 0: 
                        min_val = MIN_RAD if self.growing else MAX_RAD
                        max_val = MAX_RAD if self.growing else MIN_RAD
                        self.em.add('rad', ease_in_out_cubic, 500, min_val, max_val)
                        self.growing = not self.growing

                    elif self.slide == 1: 
                        min_val = 5 if self.closing else -H-1
                        max_val = -H-1 if self.closing else 5 
                        self.em.add('pos', ease_in_out_cubic, 500, min_val, max_val)
                        self.closing = not self.closing

                    elif self.slide == 2: 
                        min_val = 10 if self.growing2 else MAX_W
                        max_val = MAX_W if self.growing2 else 10
                        self.em.add('w', ease_in_out_cubic, 500, min_val, max_val)
                        self.growing2 = not self.growing2


                elif event.key == pg.K_RETURN: 
                    self.slide = (self.slide + 1) % self.total_slides

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
