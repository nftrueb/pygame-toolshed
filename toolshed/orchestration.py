from enum import Enum, auto 

from .vector import Vector 

class MoverState(Enum): 
    MOVING_TO_TARGET = auto()
    AT_REST = auto()

class Mover: 
    def __init__(self, x, y ): 
        self.state = MoverState.AT_REST
        self.targets = []
        self.curr_target = None
        self.target_vel = None
        self.mover_speed = 1

        self.x, self.y = x, y 

    def get_target(self):
        if len(self.targets) == 0: 
            return False 

        # pop off first target in list
        self.curr_target = self.targets[0]
        self.targets = self.targets[1:]
        if not isinstance(self.curr_target, Vector): 
            print(f'ERROR: invalid target queued for Mover: {self.curr_target}')

        # get vector for straight line from curr position to new target 
        self.target_vel = Vector(self.curr_target.x-self.x, self.curr_target.y-self.y)
        self.target_vel.norm()
        self.target_vel.scale(self.mover_speed)
        return True 
    
    def update_moving_to_target(self): 
        if self.curr_target is None and not self.get_target(): 
            return 

        # check if we are going to overstep for both x and y
        if self.target_vel.x >= 0: 
            lower, upper = self.x, self.x+self.target_vel.x 
        else: 
            lower, upper = self.x+self.target_vel.x, self.x
        x_overstep = self.is_in_inclusive_range(self.curr_target.x, lower, upper)

        if self.target_vel.y >= 0: 
            lower, upper = self.y, self.y+self.target_vel.y 
        else: 
            lower, upper = self.y+self.target_vel.y, self.y
        y_overstep = self.is_in_inclusive_range(self.curr_target.y, lower, upper)

        if x_overstep and y_overstep: 
            self.x = self.curr_target.x 
            self.y = self.curr_target.y
            self.curr_target = None 
            self.target_vel = None

            # check if new target is queued
            if not self.get_target(): 
                self.state = MoverState.AT_REST
        else: 
            self.x += self.target_vel.x 
            self.y += self.target_vel.y

    def is_in_inclusive_range(self, value, lower, upper): 
        return lower <=  value <= upper
