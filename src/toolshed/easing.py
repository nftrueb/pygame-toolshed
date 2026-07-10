from . import get_logger
from .time import get_current_millis

logger = get_logger()

def ease_in_quint(x): 
    return x**5

def ease_out_quint(x): 
    return 1 - (1 - x)**5

def ease_in_out_cubic(x):
    return 4 * x**3 if x < 0.5 else 1 - (-2 * x + 2)**3 / 2

class EaseManager: 
    def __init__(self): 
        self.eases = {}

    def get(self, tag): 
        if tag in self.eases: 
            return self.eases[tag]
        return None
    
    def add(self, tag, func, time, min_value, max_value): 
        if tag in self.eases: 
            logger.error(f'Ease obj already exists in EaseManager for tag: {tag}')
            return 
        self.eases[tag] = Ease(func, time, min_value, max_value)
    
    def update(self): 
        for ease in self.eases.values(): 
            ease.update()   
        self.eases = { k: v for k, v in self.eases.items() if not v.kill }

class Ease: 
    def __init__(self, func, target_time, min_value, max_value): 
        self.func = func 
        self.target_time = target_time
        self.min_value = min_value
        self.value_range = max_value - min_value
        self.current_time = 0 
        self.prev_update_time = get_current_millis()
        self.finished = False 
        self.kill = False

    def update(self): 
        if self.kill: 
            logger.error(f'Ease obj should have been killed already: {self}')
            return 
        
        if self.finished and not self.kill: 
            self.kill = True 
            return 
        
        self.current_time = get_current_millis() - self.prev_update_time 
        self.finished = self.current_time > self.target_time

    def get(self): 
        return self.min_value + self.value_range * self.func(self.current_time / self.target_time)