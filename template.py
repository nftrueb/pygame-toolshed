import pygame as pg

from toolshed.window import PygameContext
from toolshed.logger import Logger

WIDTH, HEIGHT = 320, 180

log = Logger()

class App: 
    def __init__(self): 
        icon = 'assets/icon.png'
        self.pc = PygameContext((WIDTH, HEIGHT), icon)
        self.running = True

    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.draw()
        except KeyboardInterrupt: 
            log.info('KeyboardInterrupt recorded... exiting now') 
        except Exception as ex: 
            log.error(f'Error encounted in main game loop: {ex}') 

        pg.quit()
        print('Successfully exited program ...') 

    def draw(self): 
        self.pc.frame.fill((255,255,255))
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
                print(f'Mouse clicked at ({mx:.{2}f}, {my:.{2}f})')

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()