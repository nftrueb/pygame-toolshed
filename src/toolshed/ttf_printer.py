import pygame as pg 
from pygame.font import Font

from toolshed import get_logger

logger = get_logger()

class ShadowDirection: 
    Left = 'Left'
    Right = 'Right', 
    Outline = 'Outline'

    def get_offset(dir: ShadowDirection): 
        if dir == ShadowDirection.Left: 
            return -1 
        elif dir == ShadowDirection.Right: 
            return 1 
        logger.error(f'Invalid direction in ShadowDirection.get_offset(): {dir}')
        return 0

class Printer: 
    def __init__(
            self, 
            font: Font, 
            color: tuple[int, int, int], 
            shadow_color: tuple[int, int, int] | None = None, 
            shadow_direction: ShadowDirection | None = None
        ): 
        self.font = font
        self.color = color
        self.shadow_color = shadow_color
        self.shadow_direction = shadow_direction 

    def print(
            self, 
            surf: pg.Surface, 
            text: str, 
            pos: tuple[int, int], 
            color: tuple[int, int, int] | None = None
        ): 
        w, h = self.font.size(text)
        if self.shadow_direction is not None:
            if self.shadow_direction == ShadowDirection.Outline: 
                shadow_surf = self.font.render(text, True, self.shadow_color)
                offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for offset in offsets: 
                    surf.blit(shadow_surf, (pos[0] + offset[0], pos[1] + offset[1]))
            else:  
                offset = ShadowDirection.get_offset(self.shadow_direction)
                shadow_surf = self.font.render(text, True, self.shadow_color)
                dest = (pos[0] + offset, pos[1])
                surf.blit(shadow_surf, dest)

        color = color if color is not None else self.color
        foreground_surf = self.font.render(text, True, color)
        surf.blit(foreground_surf, pos) 
        w, h = foreground_surf.get_size()
        return pg.Rect(pos[0], pos[1], w, h)

    def print_center(
            self, 
            surf: pg.Surface, 
            text: str, 
            pos: tuple[int, int], 
            color: tuple[int, int, int] | None = None
        ): 
        w, h = self.font.size(text)
        pos = (pos[0] - w//2, pos[1] - h//2)
        return self.print(surf, text, pos, color) 

def init_printers(printer_params): 
    fonts = {}
    printers = {}
    for name, params in printer_params.items(): 
        font_params = params['font']
        if font_params['filename'] not in fonts: 
            fonts[font_params['filename']] = pg.font.Font(**font_params)
        params['font'] = fonts[font_params['filename']]
        printers[name] = Printer(**params)
    logger.debug(f'Initialized {len(printers)} Printer objects ...')
    return printers
