import asyncio
import sys
import pygame
from {{PROJECT_APP_NAME}}.main import App

pg_submodules = [
    'font', 'mixer', 'image', 'transform', 'draw', 'time', 'event', 'display', 'surface', 'rect'
]
for sub_name in pg_submodules:
    mod = getattr(pygame, sub_name)
    if mod is not None: 
        sys.modules[f'pygame.{sub_name}'] = mod

asyncio.run(App().run())