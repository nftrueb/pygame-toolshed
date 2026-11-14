import asyncio
import profiling.tracing 
import pygame as pg
from toolshed import PICO_COLORS, toolshed_context, logger
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.gif import capture_screenshot, GifManager
from toolshed.easing import EaseManager
from toolshed.text import * 
from toolshed.profiling import save_profile_stats
from toolshed.ttf_printer import Printer
import toolshed.reload
import "PROJECT_APP_NAME".constants as c

class App: 
    def __init__(self): 
        self.pc = PygameContext((c.WIDTH, c.HEIGHT), toolshed_context.title)
        self.pm = ParticleManager()
        self.em = EaseManager()
        self.gm = GifManager()
        self.printer = 'regular'
        self.running = True

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

    def draw(self): 
        self.pc.frame.fill(PICO_COLORS.White.value)
        printer: Printer = c.printers[self.printer]
        printer.print_center(self.pc.frame, toolshed_context.appname, (c.WIDTH//2, c.HEIGHT//2))
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
    with profiling.tracing.Profile() as pr: 
        asyncio.run(App().run())
    save_profile_stats(pr)
    logger.info(green(bold('Successfully exited program ...')))

# this is not triggered if tool is installed with 'uv tool install --editable .'
if __name__ == '__main__': 
    main()
