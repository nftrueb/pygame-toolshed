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

def draw_posmover_red_rect(mover: PosMover, surf: pg.Surface): 
    pg.draw.rect(surf, (255,0,0), pg.Rect(mover.pos[0], mover.pos[1], 16, 16))
    pg.draw.rect(surf, (255,255,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16), width=1)

class App: 
    def __init__(self): 
        icon = 'assets/icon.png'
        self.pc = PygameContext((WIDTH, HEIGHT), 'Mover Demo', icon)
        self.running = True

        self.mover = PosMover((50,50), draw_posmover_rect, ease_in_out_cubic, retain_path=False)
        
        self.border_mover = PosMover((0,0), draw_posmover_rect, ease_out_quint, retain_path=True, loop=True)
        for pos in [ (WIDTH-16, 0), (WIDTH-16, HEIGHT-16), (0, HEIGHT-16), (0,0) ]: 
            self.border_mover.add_to_path(pos) 
        self.border_mover.start_animating()
    
        self.fast_mover = PosMover((16, 16), draw_posmover_red_rect, ease_out_quint, animation_frames=30, loop=True, retain_path=True)
        for pos in [ (WIDTH-16*2, 16), (WIDTH-16*2, HEIGHT-16*2), (16, HEIGHT-16*2), (16,16) ]: 
            self.fast_mover.add_to_path(pos) 
        self.fast_mover.start_animating()
        
    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.update()
                self.draw()
        except KeyboardInterrupt: 
            log.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            log.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((50,50,50))
        self.mover.draw(self.pc.frame)
        self.border_mover.draw(self.pc.frame)
        self.fast_mover.draw(self.pc.frame)
        self.pc.finish_drawing_frame()
        
    def update(self): 
        self.mover.update() 
        self.border_mover.update()
        self.fast_mover.update()
         
    def handle_event(self): 
        mx, my = self.pc.get_event_context().mouse_pos
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

                if event.key == pg.K_SPACE: 
                    try: 
                        self.fast_mover.start_animating()
                    except: 
                        pass 

            elif event.type == pg.MOUSEBUTTONDOWN: 
                # print(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')
                self.mover.add_to_path((mx, my))
                self.mover.start_animating()

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()