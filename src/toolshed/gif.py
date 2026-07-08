from datetime import datetime 
from pathlib import Path

import pygame as pg
from PIL import Image

from . import get_logger

logger = get_logger() 

class GifManager: 
    def __init__(self, speed = 25): 
        self.recording = False 
        self.frames = []
        self.speed = speed # default is 25 millis 

    def toggle(self): 
        self.recording = not self.recording
        logger.info(f'Toggled gif capturing to {self.recording}')

        if not self.recording: 
            self.save()

    def record(self, surf: pg.Surface): 
        if not self.recording: 
            return 
        
        self.frames.append(
            Image.frombytes(
                mode = 'RGB',
                  size = surf.get_size(), 
                  data = pg.image.tobytes(surf, 'RGB')
            )
        )

    def save(self): 
        if not self.frames: 
            return 
        
        filename = f'assets/output-{datetime.now()}.gif'
        self.frames[0].save(
            fp = filename, 
            save_all = True, 
            append_images = self.frames[1:], 
            duration = self.speed, 
            loop = 0 # loop infinitely 
        )
        logger.debug(f'Wrote {len(self.frames)} frames to {filename}')
        self.frames = [] # reset frames for next gif capture

def capture_screenshot(surface: pg.Surface, filename: str | None = None): 
    output_dir = Path('output')
    if filename is None: 
        if not output_dir.exists() or not output_dir.is_dir(): 
            output_dir.mkdir()
            logger.info(f'Created new directory: {output_dir.name}')
        filename = output_dir / f'screenshot-{datetime.now()}.png'

    Image.frombytes(
        'RGB', 
        surface.get_size(), 
        pg.image.tobytes(surface, 'RGB')
    ).save(filename)

    logger.info(f'Saved screenshot to {filename}')