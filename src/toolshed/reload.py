import os 
import importlib
import sys
import inspect
import gc
import time
import types
import ast

from toolshed import logger
from toolshed.threads import ToolshedThread, ToolshedThreadPool, consolidate_threads

def _get_file_update_time(file): 
    return os.stat(file).st_mtime 

def _get_classes_of(module): 
    return {
        name: cls for name, cls in vars(module).items()
        if (inspect.isclass(cls) and cls.__module__ == module.__name__) or type(cls) == type
    }

def _compile_python(filename: str): 
    try: 
        with open(filename, 'r') as f: 
            contents = f.read() 
        ast.parse(contents)
        return True
    except Exception as ex: 
        pass 
    return False 

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
        self.log_timer = 0 

    def run(self):
        try: 
            while not self.thread_event.is_set(): 
                self.watch_loop()
        except Exception as ex: 
            logger.error('Fatal exception occurred in Reloader thread', ex) 

    def watch_loop(self):  
        target = self.module_data_list[self.curr_module_idx]
        st_mtime = _get_file_update_time(target.file)
        if st_mtime != target.st_mtime: 
            try: 
                self.attempt_module_reload(target)
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

        # debug log on timer
        now = time.time() 
        if now - self.log_timer > Reloader.LOG_TIMER: 
            # logger.debug('Reloader still running ....')
            self.log_timer = now

    def attempt_module_reload(self, target: ModuleData): 
        # get references to all classes in module 
        old_classes = _get_classes_of(target.module)

        # check that file has valid python syntax 
        if _compile_python(target.file): 

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
                elif type(obj) == type and obj in class_transition_map: 
                    obj = class_transition_map[obj]

            logger.info(f'{target.module.__name__} successfully reloaded')
        else: 
            logger.debug(f'Tried to reload {target.name} but source didn\'t compile')

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

pool = ToolshedThreadPool(Reloader) 
pool.start()
consolidate_threads(ToolshedThreadPool.THREAD_NAME)
