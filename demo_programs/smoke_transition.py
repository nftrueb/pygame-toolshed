import asyncio
import random

import pygame as pg

from toolshed import get_logger
from toolshed.window import PygameContext
from toolshed.particles import ParticleManager
from toolshed.shapes import Circle

WIDTH, HEIGHT = 128, 128

logger = get_logger()

class SmokeTransition: 
    def __init__(self): 
        self.circles = [ SmokeTransition.build_circle() for _ in range(100)]

    def build_circle(): 
        min_rad = 12
        max_rad = 16
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        rad = random.randint(min_rad, max_rad) 
        color = random.choice([(100,100,100), (200, 200, 200), (250,250,250)])
        return Circle(x, y, rad, color )

    def update(self): 
        if len(self.circles) == 0:
            return 
        
        for c in self.circles: 
            # shrink rad
            if random.random() > 0.5: 
                c.rad -= 1

            # float up
            c.y -= 1 

            # randomly move left/right
            dir =  random.random()
            if dir > 0.9: 
                c.x += 1
            elif dir < 0.1: 
                c.x -= 1

        # filter out circles that disappeared
        self.circles = list(filter(lambda x: x.rad > 0, self.circles)) 

    def draw(self, surf): 
        for c in self.circles:
            c.draw(surf)

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT), 'Transition Demo', icon_path='./assets/icon.png')
        self.pm = ParticleManager()
        self.running = True

        self.state = True
        self.smoke_transition = None

        logger.debug(f'{self.pc.base_dims} {self.pc.screen_dims}')

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
        colors = {
            True: (150,255,150), 
            False: (255, 150, 150)
        }
        self.pc.frame.fill(colors[self.state])

        if self.smoke_transition is not None: 
            self.smoke_transition.draw(self.pc.frame)

        self.pm.draw(self.pc.frame)
        self.pc.finish_drawing_frame()

    def update(self): 
        if self.smoke_transition is not None: 
            self.smoke_transition.update()
        self.pm.update()

    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

                elif event.key == pg.K_SPACE: 
                    self.state = not self.state
                    self.smoke_transition = SmokeTransition()

            elif event.type == pg.MOUSEBUTTONUP: 
                logger.debug(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')
                

def main(): 
    asyncio.run(App().run())

if __name__ == '__main__': 
    main()
