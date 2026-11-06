import re 

ANSI_CODE_RE = r'(?:\x1B[@-Z\\-_]|\x1B\[[0-?]*[ -/]*[@-~])'
PREFIX = '\033['
SUFFIX = 'm'
RESET = '\033[0m'
BOLD = '1'
RED = '31'
GREEN = '32'

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
