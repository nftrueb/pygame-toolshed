from pathlib import Path 
import os 
import importlib
import sys

from toolshed import get_logger

logger = get_logger()

def _get_file_update_time(file): 
    return os.stat(file).st_mtime 

class ReloaderModule: 
    def __init__(self, package, module_name): 
        self.package = package
        self.module = f'{package}.{module_name}'
        self.file = f'src/{package}/{module_name}.py'
        self.st_mtime = _get_file_update_time(self.file)

class Reloader: 
    EXCLUSIONS = {'main'}
    def __init__(self, dir: Path, package): 
        self.package = package
        self.curr_module_idx = 0
        module_names = list(filter(
            lambda x: x not in Reloader.EXCLUSIONS, 
            [ str(file).split('/')[-1][:-3] for file in dir.rglob('*.py') ]
        ))
        self.modules = [ ReloaderModule(package, module) for module in module_names ]
        logger.info(f'Registered {len(self.modules)} modules in the Reloader')

    def try_reloading(self):
        target = self.modules[self.curr_module_idx]
        st_mtime = _get_file_update_time(target.file)
        if st_mtime != target.st_mtime: 
            try: 
                importlib.reload(sys.modules[target.module])
                target.st_mtime = st_mtime
                logger.info(f'{target.module} successfully reloaded')
            except Exception as ex: 
                pass
        self.curr_module_idx = (self.curr_module_idx + 1) % len(self.modules)
