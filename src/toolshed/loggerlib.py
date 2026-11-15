import traceback
from toolshed.text import * 
from toolshed.singleton import Singleton

class Level: 
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    ERROR = 'ERROR'
    TODO = 'TODO'

class Logger(Singleton): 
    PREFIX_LEN = max([ len(v) for k, v in Level.__dict__.items() if not k.startswith('__')]) 

    def prefix(self, level): 
        s = f'[ {level}'
        s += ''.join([ ' ' for _ in range(Logger.PREFIX_LEN - len(level) )])
        s += ' ] '
        if level == Level.ERROR: 
            s = red(s)
        elif level == Level.TODO: 
            s = blue(s) 
        return s

    def debug(self, message): 
        self.log(Level.DEBUG, message)  

    def info(self, message): 
        self.log(Level.INFO, message)  

    def error(self, message, ex: BaseException = None): 
        message = red(bold(message))
        if ex is not None: 
            message += ':' + bold(f'\n{ex.__class__.__name__}: {ex}\n')
            first_frame = True
            for frame in reversed(traceback.extract_tb(ex.__traceback__)): 
                frame_line = f'  {frame.filename}::{frame.lineno}'
                message += bold(frame_line) if first_frame else frame_line
                message += '\n'
                first_frame = False
            message = message[:-1]
        self.log(Level.ERROR, message) 

    def todo(self, message): 
        self.log(Level.TODO, bold(blue(message)))

    def log(self, level, input_msg):
        # input message can be any object ... must cast to string first
        s = str(input_msg)
        prefix = bold(self.prefix(level))
    
        # construct a white space string so that multi-line messages can be left aligned
        whitespace_prefix = '\n' + ''.join([' ' for _ in range(len_stripped(prefix))])
        formatted_message = whitespace_prefix.join(s.split('\n'))

        # print final prefix and message
        print(f'{prefix}{formatted_message}')

logger = Logger()
