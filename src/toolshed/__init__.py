from enum import StrEnum, auto
import sys
from collections.abc import Callable 
from toolshed.loggerlib import Logger
from toolshed.singleton import Singleton

logger = Logger() 

class SystemType(StrEnum): 
    Darwin = auto()

class ToolshedContext(Singleton):  
    def __init__(self): 
        # define the project root path to perform path operations regardless of current directory
        segments = __file__.split('/')[:-4]
        segments.append('')
        self.project_dir = '/'.join(segments)

        # define current OS 
        self.platform = SystemType(sys.platform)

        # app details 
        self.appname = ''
        self.title = ''
        self.root_dir_name = ''

    def __str__(self): 
        s  = f'ToolshedContext(\n'
        s += f'  project_dir={self.project_dir}\n'
        s += f'  platform={self.platform}\n'
        s += f')'
        return s
    
    def get_root_dir(self): 
        return f'{self.project_dir}{self.root_dir_name}/'

# Classes to be moved to color.py
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

# Helpers
def attempt(fn: Callable, *args, print_exception=False): 
    try: 
        fn(*args)
    except BaseException as ex: 
        if print_exception: 
            logger.error(f'Exception when attempting {fn.__name__}', ex)

# Singletons
logger = Logger()
toolshed_context = ToolshedContext()
logger.debug(toolshed_context) 
print(logger)
# sys.exit()

# Constants
MAX_INT = (1 << 31) - 1
MIN_INT = -(1 << 31)
DEFAULT_PICO8_FONT_SIZE = 5
PICO8_DIMS = (128, 128)