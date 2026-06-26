from enum import StrEnum, auto

from .logger import Logger 

logger = Logger()
def get_logger(): 
    return logger

class SystemType(StrEnum): 
    Darwin = auto()