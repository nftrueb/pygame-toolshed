from pathlib import Path 
import os 
import importlib
import sys
import inspect
import gc
import threading
import atexit
import time

from toolshed import get_logger

logger = get_logger()

def _get_file_update_time(file): 
    return os.stat(file).st_mtime 

def _get_classes_of(module): 
    return {
        name: cls for name, cls in vars(module).items()
        if (inspect.isclass(cls) and cls.__module__ == module.__name__) or type(cls) == type
    }

class ModuleData: 
    def __init__(self, module): 
        self.module = module 
        self.st_mtime = _get_file_update_time(module.__file__)

class Reloader(threading.Thread): 
    EXCLUSIONS = {'main'}

    def __init__(self): 
        super().__init__(daemon=True)
        changing_modules = [ 
            m for m in sys.modules.values() 
            if hasattr(m, '__file__') 
            and m.__file__.startswith('/'.join(__file__.split('/')[:-4]))
        ]
        self.module_to_update_time = [ ModuleData(m) for m in changing_modules ]
        self.curr_module_idx = 0
        logger.info(f'Registered {len(self.module_to_update_time)} modules in the Reloader')

    def run(self):
        now = time.time()
        while True: 
            target = self.module_to_update_time[self.curr_module_idx]
            st_mtime = _get_file_update_time(target.module.__file__)
            if st_mtime != target.st_mtime: 
                try: 
                    # get references to all classes in module 
                    old_classes = _get_classes_of(target.module)

                    # reload module 
                    importlib.reload(target.module)

                    # set map of old references to new references
                    new_classes =  _get_classes_of(target.module)
                    class_transition_map = {
                        old: new_classes[name] for name, old in old_classes.items()
                    }
                    
                    # loop over objects and reassign __class__ to the new ref
                    for obj in gc.get_objects(): 
                        if type(obj) in class_transition_map.keys(): 
                            obj.__class__ = class_transition_map[type(obj)]
                            print(f'Matched ' + str(obj))
                        elif type(obj) == type and obj in class_transition_map: 
                            obj = class_transition_map[obj]

                    logger.info(f'{target.module.__name__} successfully reloaded')

                finally: 
                    # reset update time
                    target.st_mtime = st_mtime

            # increment idx to change watched file for the next step
            self.curr_module_idx = (self.curr_module_idx + 1) % len(self.module_to_update_time)

            # delay before checking the next module ... each module is checked once a second
            time.sleep(1 / len(self.module_to_update_time))

            if time.time() - now > 5: 
                logger.debug('Reloader still running .... ')
                now = time.time()

reloader = Reloader()
reloader.start()
