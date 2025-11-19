import pygame as pg 
from pygame import Window

from toolshed.window import PygameContext

WIDTH, HEIGHT = (320, 180)

def main(): 
    pg.init()

    pc = PygameContext((WIDTH, HEIGHT))
    window = Window('Window Demo', pc.screen.get_size())

    running = True 
    while running: 
        for event in pg.event.get(): 
            if event.type == pg.WINDOWCLOSE: 
                event.window.destroy()

            elif event.type == pg.QUIT: 
                running = False 

            elif event.type == pg.MOUSEBUTTONUP: 
                window.flash(pg.FLASH_BRIEFLY)

        pc.frame.fill((0,0,0))

        pc.finish_drawing_frame() 

    pg.quit()
    print('Successfully exited program ...')

if __name__ == '__main__': 
    main()