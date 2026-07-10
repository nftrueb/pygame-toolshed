from time import time_ns

def get_current_millis(): 
    return time_ns() // 1_000_000