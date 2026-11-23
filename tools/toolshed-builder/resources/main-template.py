import asyncio
import pygame as pg
from toolshed import PICO_COLORS, toolshed_context, logger
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager, PulseParticle
from toolshed.easing import EaseManager, ease_out_quint
from toolshed.text import * 
from toolshed.ttf_printer import Printer
from toolshed.vector import Vector
import {{PROJECT_APP_NAME}}.constants as c

if toolshed_context.is_desktop_version(): 
    import profiling.tracing
    from toolshed.profiling import save_profile_stats
    import toolshed.reload
    # from toolshed.gif import capture_screenshot, GifManager

class App: 
    def __init__(self): 
        self.pc = PygameContext((c.WIDTH, c.HEIGHT), toolshed_context.title)
        self.running = True
        self.pm = ParticleManager()
        self.em = EaseManager()
        self.em.add('rad-change', ease_out_quint, 3000, 40, 60)

    async def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
                self.update()
                await asyncio.sleep(0)
        except (asyncio.CancelledError, KeyboardInterrupt): 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except BaseException as ex: 
            logger.error(f'Error encounted in main game loop', ex) 
        finally: 
            self.pc.quit()
        logger.info(green(bold('Successfully exited program ...')))

    def draw(self): 
        printer: Printer = c.printers['p8']
        self.pc.frame.fill(PICO_COLORS.Brown.value)
        rad = self.em.get('rad-change')
        pg.draw.circle(
            self.pc.frame, 
            PICO_COLORS.Peach.value, 
            (c.WIDTH//2, c.HEIGHT//2), 
            radius= 50 if rad is None else rad.get()
        )
        printer.print_center(
            surf=self.pc.frame, 
            text=toolshed_context.appname, 
            pos=(c.WIDTH//2, c.HEIGHT//2), 
            color=PICO_COLORS.DarkBlue.value
        )
        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()

    def update(self): 
        self.pm.update()
        self.em.update()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False

                elif event.key == pg.K_r: 
                    # reload program
                    pass 

            elif event.type == pg.MOUSEBUTTONUP: 
                self.pm.add_particle(
                    PulseParticle(
                        pos=Vector(mx, my), 
                        vel=Vector(0,0), 
                        timer=45, 
                        color=PICO_COLORS.DarkBlue.value
                    )
                )
                if event.button == pg.BUTTON_LEFT:
                    logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

def main(): 
    if toolshed_context.is_desktop_version(): 
        with profiling.tracing.Profile() as pr: 
            asyncio.run(App().run())
        save_profile_stats(pr)

    elif toolshed_context.is_web_version(): 
        asyncio.run(App().run())
        
    else: 
        logger.error(f'Running in unsupported platform: {toolshed_context.platform}')

# entry point for app bundle
if __name__ == '__main__': 
    main()
