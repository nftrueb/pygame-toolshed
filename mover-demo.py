import traceback
from pathlib import Path

import pygame as pg

from toolshed.window import PygameContext
from toolshed.logger import Logger
from toolshed.orchestration import PosMover, ease_in_out_cubic, ease_out_quint, ease_in_quint

WIDTH, HEIGHT = 320, 180

log = Logger(Path(__file__).resolve().parent)

# easing functions have a graph of some y value between an x value of 0 and 1
# x value should always be time ... define an animation event in terms of x frames or millis 
# y value can be mapped to behavior such as position, size, transparency
# in middle of animation, check current time as percentage of goal time 
# use that value in easing function to get corresponding y value 
# use that value in whatever application has been chosen 

def draw_posmover_rect(mover: PosMover, surf: pg.Surface): 
    pg.draw.rect(surf, (0,0,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16))
    pg.draw.rect(surf, (255,255,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16), width=1)

class App: 
    def __init__(self): 
        icon = 'assets/icon.png'
        self.pc = PygameContext((WIDTH, HEIGHT), 'Mover Demo', icon)
        self.running = True

        self.mover = PosMover((50,50), draw_posmover_rect, ease_in_out_cubic)

    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.update()
                self.draw()
        except KeyboardInterrupt: 
            log.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            tb = ex.__traceback__
            log.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((50,50,50))
        self.mover.draw(self.pc.frame)
        self.pc.finish_drawing_frame()
        
    def update(self): 
        self.mover.update() 
         
    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

                if event.key == pg.K_SPACE: 
                    if self.mover.easing_fn == ease_in_out_cubic: 
                        self.mover.easing_fn = ease_out_quint
                    else: 
                        self.mover.easing_fn = ease_in_out_cubic

            elif event.type == pg.MOUSEBUTTONDOWN: 
                # print(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')
                self.mover.start_animating((mx, my))

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()