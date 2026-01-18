class Logger: 
    class Level: 
        DEBUG = 'DEBUG'
        INFO = 'INFO'
        ERROR = 'ERROR'

    def debug(self, message): 
        self.log(self.Level.DEBUG, message)  

    def info(self, message): 
        self.log(self.Level.INFO, message)  

    def error(self, message): 
        self.log(self.Level.ERROR, message) 

    def log(self, level, message): 
        print(f'[ {level} ] {message}')
