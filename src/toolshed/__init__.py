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