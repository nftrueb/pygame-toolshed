import pygame as pg

from toolshed.window import PygameContext, EventContext

WIDTH, HEIGHT = 320, 180

class App: 
    def __init__(self): 
        icon = 'assets/icon.png'
        self.pc = PygameContext((WIDTH, HEIGHT), icon)
        self.ec = EventContext((0,0))
        self.running = True

    def run(self): 
        try: 
            while self.running: 
                self.ec = self.pc.get_event_context()
                self.step_frame()

        except KeyboardInterrupt: 
            pass 

        pg.quit()
        print('Successfully exited program ...') 

    def step_frame(self): 
        self.handle_event()

        self.pc.frame.fill((255,255,255))

        self.pc.finish_drawing_frame()

    def handle_event(self): 
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False 

            elif event.type == pg.MOUSEBUTTONUP: 
                print(f'Mouse clicked at ({self.ec.mouse_pos})')

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()