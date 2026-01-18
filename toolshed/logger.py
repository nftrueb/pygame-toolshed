from pathlib import Path

class Logger: 
    class Level: 
        DEBUG = 'DEBUG'
        INFO = 'INFO'
        ERROR = 'ERROR'

    def __init__(self, root: Path): 
        self.root = root.__str__()

    def prefix(self, level): 
        return f'[ {level} ] '

    def debug(self, message): 
        self.log(self.Level.DEBUG, message)  

    def info(self, message): 
        self.log(self.Level.INFO, message)  

    def error(self, message, ex: Exception): 
        message += f': {ex}\n'
        frame = ex.__traceback__
        while frame is not None: 
            filename = frame.tb_frame.f_code.co_filename
            if filename.startswith(self.root): 
                filename = filename[len(self.root)+1:]
            message += f'Line: {frame.tb_lineno} -- {frame.tb_frame.f_code.co_name} -- {filename}\n'
            frame = frame.tb_next
        self.log(self.Level.ERROR, message[:-1]) 

    def log(self, level, input_msg): 
        prefix = self.prefix(level)
        whitespace_prefix = '\n' + ''.join([' ' for i in range(len(prefix))])
        constructed_msg = whitespace_prefix.join(input_msg.split('\n'))
        print(f'{prefix}{constructed_msg}')
