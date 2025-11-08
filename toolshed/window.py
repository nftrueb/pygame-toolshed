import pygame as pg 
from dataclasses import dataclass 
from typing import Tuple

def get_window_scale(base_size, scaled_size):
        return min(scaled_size[0] // base_size[0], scaled_size[1] // base_size[1])

@dataclass
class EventContext:
    mouse_pos: Tuple[float, float] = (0,0)

class PygameContext: 
    def __init__(self, base_dims, icon=None): 
        pg.init()

        # record the base dimensions as separate vars 
        self.base_dims = base_dims
        
        # get monitor info and record the scale and screen dimensions
        info = pg.display.Info()
        self.scale = get_window_scale(base_dims, (info.current_w * .7, info.current_h))
        self.scaled_dims = (base_dims[0] * self.scale, base_dims[1] * self.scale)
        self.screen_dims = self.scaled_dims

        # instantiate screen object 
        self.screen = pg.display.set_mode(self.scaled_dims, pg.RESIZABLE)
        self.frame = pg.Surface(self.screen.get_size())
        self.clock = pg.Clock() 

        if icon is not None: 
            icon_surf = None
            try: 
                icon_surf = pg.image.load(icon)
            except: 
                print(f'[ INFO ] Failed to load icon image at path: {icon}')
            
            if icon_surf is not None:
                pg.display.set_icon(pg.image.load(icon))

    def finish_drawing_frame(self): 
        scaled_frame = pg.transform.scale(self.frame, self.scaled_dims)
        fw, fh = self.scaled_dims
        sw, sh = self.screen_dims

        self.screen.fill((0,0,0))
        self.screen.blit(scaled_frame, ((sw-fw)/2, (sh-fh)/2))
        pg.display.update()
        self.clock.tick(60)

    def get_scaled_mouse_pos(self): 
        mx, my = pg.mouse.get_pos()
        sw, sh = self.screen_dims
        fw, fh = self.scaled_dims
        bufx, bufy = (sw - fw) / 2, (sh - fh) /2

        mx = (mx - bufx) / self.scale
        my = (my - bufy) / self.scale 

        return (mx, my)
    
    def get_event_context(self) -> EventContext: 
        return EventContext(self.get_scaled_mouse_pos())
