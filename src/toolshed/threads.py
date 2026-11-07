import threading
from toolshed.logger import logger
from toolshed.time import get_current_millis

def get_threads() -> list[ToolshedThread]:
    return [ t for t in threading.enumerate() if isinstance(t, ToolshedThread)]

def get_threads_by_name(name='') -> list[ToolshedThread]: 
    return list(filter(lambda thread: thread.name == name, get_threads()))

def consolidate_threads(name=None, n=1) -> None: 
    if name is None: 
        logger.error('Specify name of threads to consolidate')
        return 
    threads = get_threads_by_name(name)
    threads.sort()
    last_idx = -1 * n
    for t in threads[:last_idx]: 
        t.kill()
    logger.debug(f'Consolidated {name} threads to {n}')

class ToolshedThread(threading.Thread): 
    def __init__(self, name='ToolshedThread'):
        super().__init__(daemon=True, name=name) 
        self.class_name = self.__class__.__name__
        self.thread_event = threading.Event()
        self.start_time = None 
        logger.info(f'{self.class_name} thread starting ...') 

    def __lt__(self, other: ToolshedThread): 
        return self.start_time < other.start_time 

    def __str__(self): 
        return f'{self.__class__.__name__}(name={self.name}, start_time={self.start_time})'

    def start(self): 
        logger.info(f'{self.class_name} thread starting ...') 
        super().start()
        self.start_time = get_current_millis()

    def kill(self): 
        self.thread_event.set()
        logger.debug(f'Killing {str(self)}')

# class SubclassThread(ToolshedThread): 
#     NAME = 'SubclassThread'
#     def __init__(self): 
#         super().__init__(name=SubclassThread.NAME) 

#     def run(self): 
#         while not self.thread_event.is_set(): 
#             pass 
