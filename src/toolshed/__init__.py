from enum import StrEnum, auto

from .logger import Logger 

logger = Logger()
def get_logger(): 
    return logger

class SystemType(StrEnum): 
    Darwin = auto()

MAX_INT = (1 << 31) - 1
MIN_INT = -(1 << 31)
DEFAULT_PICO8_FONT_SIZE = 5
PICO8_DIMS = (128, 128)


class Color: 
    def __init__(self, name: str, value: tuple[int, int, int]): 
        self.name = name
        self.value = value

class PICO_COLORS: 
    Black = Color('Black', (0, 0, 0))
    DarkBlue = Color('DarkBlue', (29, 43, 83))
    DarkPurple = Color('DarkPurple', (126, 37, 83))
    DarkGreen = Color('DarkGreen', (0, 135, 81))
    Brown = Color('Brown', (171, 82, 54))
    DarkGray = Color('DarkGray', (95, 87, 79))
    LightGray = Color('LightGray',  (194, 195, 199))
    White = Color('White',  (255, 241, 232))
    Red = Color('Red',  (255, 0, 77))
    Orange = Color('Orange',  (255, 163, 0))
    Yellow = Color('Yellow',  (255, 236, 39))
    Green = Color('Green',  (0, 228, 54))
    Blue = Color('Blue',  (41, 173, 255))
    Indigo = Color('Indigo',  (131, 118, 156))
    Pink = Color('Pink',  (255, 119, 168))
    Peach = Color('Peach',  (255, 204, 170))
