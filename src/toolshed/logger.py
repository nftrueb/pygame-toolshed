import os
import traceback
from toolshed.text import * 

class Level: 
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    ERROR = 'ERROR'

class Logger: 
    PREFIX_LEN = max([ len(v) for k, v in Level.__dict__.items() if not k.startswith('__')]) 

    def __init__(self): 
        env = os.environ
        self.root = None
        if 'PYGAME_TOOLSHED_LOGGER_ROOT' in env.keys(): 
            self.root = env.get('PYGAME_TOOLSHED_LOGGER_ROOT')
            self.debug(f'Logger initialized with root: {self.root}')

    def prefix(self, level): 
        s = f'[ {level}'
        s += ''.join([ ' ' for _ in range(Logger.PREFIX_LEN - len(level) )])
        s += ' ] '
        return red(s) if level == Level.ERROR else s

    def debug(self, message): 
        self.log(Level.DEBUG, message)  

    def info(self, message): 
        self.log(Level.INFO, message)  

    def error(self, message, ex: BaseException = None): 
        message = red(bold(message))
        if ex is not None: 
            message += ':' + bold(f'\n{ex.__class__.__name__}: {ex}\n')
            for frame in reversed(traceback.extract_tb(ex.__traceback__)): 
                segments = frame.filename.split('/')
                message += f'  {'/'.join(segments[:-1])}/'
                message += bold(f'{segments[-1]}::{frame.lineno}')
                message += '\n'
            message = message[:-1]
        self.log(Level.ERROR, message) 

    def log(self, level, input_msg): 
        prefix = bold(self.prefix(level))
        whitespace_prefix = '\n' + ''.join([' ' for _ in range(len_stripped(prefix))])
        constructed_msg = whitespace_prefix.join(input_msg.split('\n'))
        print(f'{prefix}{constructed_msg}')
