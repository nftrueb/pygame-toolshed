import os 
import importlib
import sys
import inspect
import gc
import time
import types

from toolshed.logger import logger
from toolshed.threads import ToolshedThread, consolidate_threads, get_threads_by_name

def _get_file_update_time(file): 
    return os.stat(file).st_mtime 

def _get_classes_of(module): 
    return {
        name: cls for name, cls in vars(module).items()
        if (inspect.isclass(cls) and cls.__module__ == module.__name__) or type(cls) == type
    }

class ModuleData: 
    def __init__(self, module: types.ModuleType): 
        self.module = module 
        self.name = module.__name__
        self.file = module.__file__
        self.st_mtime = _get_file_update_time(self.file)

class Reloader(ToolshedThread): 
    LOG_TIMER = 10
    THREAD_NAME = 'reloader'

    def __init__(self): 
        super().__init__(name=Reloader.THREAD_NAME)
        self.module_data_list = []
        self.curr_module_idx = 0
        self.prev_sys_modules_length = 0
        self.check_for_new_modules()

    def run(self):
        now = time.time()
        while not self.thread_event.is_set(): 
            target = self.module_data_list[self.curr_module_idx]
            st_mtime = _get_file_update_time(target.file)
            if st_mtime != target.st_mtime: 
                try: 
                    # get references to all classes in module 
                    old_classes = _get_classes_of(target.module)

                    # reload module 
                    importlib.reload(target.module)

                    if target.name == 'toolshed.reload': 
                        consolidate_threads(self.name)

                    # set map of old references to new references
                    new_classes =  _get_classes_of(target.module)
                    class_transition_map = {
                        old: new_classes[name] for name, old in old_classes.items()
                    }
                    
                    # loop over objects and reassign __class__ to the new ref
                    for obj in gc.get_objects(): 
                        if type(obj) in class_transition_map.keys(): 
                            obj.__class__ = class_transition_map[type(obj)]
                        elif type(obj) == type and obj in class_transition_map: 
                            obj = class_transition_map[obj]

                    logger.info(f'{target.module.__name__} successfully reloaded')

                finally: 
                    # reset update time
                    target.st_mtime = st_mtime

            # increment idx to change watched file for the next step
            self.curr_module_idx = (self.curr_module_idx + 1) % len(self.module_data_list)

            # delay before checking the next module ... each module is checked once a second
            time.sleep(1 / len(self.module_data_list))

            # check for new modules after each cycle
            if self.curr_module_idx == 0: 
                self.check_for_new_modules()

            if time.time() - now > Reloader.LOG_TIMER: 
                logger.debug('Reloader still running .... ')
                now = time.time()

    def check_for_new_modules(self): 
        modules = sys.modules.values()
        if len(modules) == self.prev_sys_modules_length: 
            return 
        self.prev_sys_modules_length = len(modules)
        
        modules_to_watch = [ 
            m for m in sys.modules.values() 
            if hasattr(m, '__file__') 
            and isinstance(m.__file__, str)
            and m.__file__.startswith('/'.join(__file__.split('/')[:-4]))
        ]
        self.module_data_list = [ ModuleData(m) for m in modules_to_watch ]
        self.curr_module_idx = 0 
        logger.debug(f'Reloader initialized {len(self.module_data_list)} modules')

# this can be anonamous since it runs fully autonamously 
Reloader().start()
