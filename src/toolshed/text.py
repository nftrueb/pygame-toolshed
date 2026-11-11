import re 
import sys

_logger = None
def get_logger(): 
    global _logger
    if _logger is None: 
        try: 
            from toolshed import logger 
            _logger = logger 
        except ImportError as ex: 
            print(f'Failed to import logger in toolshed.text: {ex}') 
            sys.exit()
    return _logger

ANSI_CODE_RE = r'(?:\x1B[@-Z\\-_]|\x1B\[[0-?]*[ -/]*[@-~])'
PREFIX = '\033['
SUFFIX = 'm'
RESET = '\033[0m'
BOLD = '1'
RED = '31'
GREEN = '32'
WHITE = '37'

def len_stripped(s: str): 
    return len(re.sub(re.compile(ANSI_CODE_RE), '', s))

def reset(s: str): 
    return f'{s}{RESET}'

def encode_effect(s: str, effect: str): 
    return f'{PREFIX}{effect}{SUFFIX}{s}{RESET}'

def bold(s: str): 
    return encode_effect(s, BOLD)

def red(s: str): 
    return encode_effect(s, RED)

def green(s: str): 
    return encode_effect(s, GREEN) 

def white(s: str): 
    return encode_effect(s, WHITE) 

def remove_prefix(s: str, prefix: str) -> str: 
    get_logger().info(f'toolshed.text.remove_prefix')
    if s.startswith(prefix): 
        return ''.join(s.split(prefix)[1:])
    get_logger().info(f'toolshed.text.remove_prefix: Tried to remove {prefix} from {s}')
    return s
