import traceback
from pathlib import Path

import pygame as pg

from toolshed import get_logger
from toolshed.window import PygameContext
from toolshed.orchestration import PosMover, ease_in_out_cubic, ease_out_quint, ease_in_quint

WIDTH, HEIGHT = 320, 180

logger = get_logger()

BOX_W, BOX_H = WIDTH * .9, HEIGHT * .9
BOX_X, BOX_Y = (WIDTH - BOX_W ) / 2, (HEIGHT - BOX_H) / 2
box = pg.Rect(BOX_X, BOX_Y, BOX_W, BOX_H)

# easing functions have a graph of some y value between an x value of 0 and 1
# x value should always be time ... define an animation event in terms of x frames or millis 
# y value can be mapped to behavior such as position, size, transparency
# in middle of animation, check current time as percentage of goal time 
# use that value in easing function to get corresponding y value 
# use that value in whatever application has been chosen 

def draw_blue(mover: PosMover, surf: pg.Surface): 
    pg.draw.rect(surf, (0,0,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16))
    pg.draw.rect(surf, (255,255,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16), width=1)

def draw_red(mover: PosMover, surf: pg.Surface): 
    pg.draw.rect(surf, (255,0,0), pg.Rect(mover.pos[0], mover.pos[1], 16, 16))
    pg.draw.rect(surf, (255,255,255), pg.Rect(mover.pos[0], mover.pos[1], 16, 16), width=1)

class App: 
    def __init__(self): 
        icon = 'assets/icon.png'
        self.pc = PygameContext((WIDTH, HEIGHT), 'Mover Demo', icon)
        self.running = True

        self.mover = PosMover((50,50), ease_in_out_cubic, retain_path=False)
        
        self.border_mover = PosMover((0,0), ease_out_quint, retain_path=True, loop=True)
        for pos in [ (WIDTH-16, 0), (WIDTH-16, HEIGHT-16), (0, HEIGHT-16), (0,0) ]: 
            self.border_mover.add_to_path(pos) 
        self.border_mover.start_animating()
    
        self.fast_mover = PosMover((16, 16), ease_out_quint, animation_frames=30, loop=True, retain_path=True)
        for pos in [ (WIDTH-16*2, 16), (WIDTH-16*2, HEIGHT-16*2), (16, HEIGHT-16*2), (16,16) ]: 
            self.fast_mover.add_to_path(pos) 
        self.fast_mover.start_animating()

        self.box = pg.Rect(WIDTH * .05 , HEIGHT * .05, WIDTH * .9, HEIGHT * .9)
        self.box_mover = PosMover((self.box.x, self.box.y), ease_in_out_cubic, retain_path=True)
        self.box_mover.path = [
            (self.box.x, self.box.y), 
            (self.box.x, -self.box.h)
        ]
        self.box_mover.active = True
        
    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.update()
                self.draw()
        except KeyboardInterrupt: 
            logger.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            logger.error(f'Error encounted in main game loop', ex) 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((50,50,50))
        draw_blue(self.mover, self.pc.frame)
        draw_blue(self.border_mover, self.pc.frame) 
        draw_red(self.fast_mover, self.pc.frame) 

        # draw the box variable 
        pos = self.box_mover.pos
        pg.draw.rect(self.pc.frame, (0,0,0), (pos[0], pos[1], self.box.w, self.box.h))
        pg.draw.rect(self.pc.frame, (100,100,100), self.box, width=1)

        self.pc.finish_drawing_frame()
        
    def update(self): 
        self.mover.update() 
        self.border_mover.update()
        self.fast_mover.update()
        self.box_mover.update()
         
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
                        self.box_mover.start_animating()
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