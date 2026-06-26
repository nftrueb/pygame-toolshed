import pygame as pg 

from toolshed.window import PygameContext 
from toolshed.orchestration import Animation

WIDTH, HEIGHT = 320, 180

class App: 
    def __init__(self): 
        self.pc = PygameContext((WIDTH, HEIGHT)) 
        self.running = True 

        font_image = pg.image.load('assets/font.png').convert_alpha()
        sprites = [ (font_image.subsurface(pg.Rect(8*i,8,8,8)), 60) for i in range(10) ]
        self.animation = Animation(sprites)

    def run(self): 
        try: 
            while self.running: 
                self.handle_event()
                self.update()
                self.draw()

        except KeyboardInterrupt: 
            pass 

        self.pc.quit()
        print('Successfully exited program ....')

    def handle_event(self): 
        ec = self.pc.get_event_context()
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False 

            elif event.type == pg.KEYUP: 
                if event.key == pg.K_ESCAPE: 
                    self.running = False  

                if event.key == pg.K_SPACE: 
                    self.animation.toggle()

    def update(self): 
        self.animation.update()

    def draw(self): 
        self.pc.frame.fill((50,50,50))

        surf = self.animation.get_current_sprite()
        if surf is not None: 
            self.pc.frame.blit(surf, (50, 50))

        self.pc.finish_drawing_frame()

def main(): 
    app = App()
    app.run()

if __name__ == '__main__': 
    main()