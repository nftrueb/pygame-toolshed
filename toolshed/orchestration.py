def ease_in_quint(x): 
    return x**5

def ease_out_quint(x): 
    return 1 - (1 - x)**5

def ease_in_out_cubic(x):
    return 4 * x**3 if x < 0.5 else 1 - (-2 * x + 2)**3 / 2

class Mover: 
    def __init__(self, draw_fn, easing_fn, animation_frames=60): 
        self.draw_fn = draw_fn
        self.easing_fn = easing_fn
        
        self.animating = False
        self.animation_frames = 60
        self.frames = 0 

    def update(self): 
        if not self.animating: 
            return 
        
        self.frames += 1
        if self.frames >= self.animation_frames: 
            self.stop_animating()

    def get_easing_value(self): 
        return self.easing_fn(self.frames / self.animation_frames) if self.animating else None

    def start_animating(self): 
        self.animating = True
        self.frames = 0 

    def stop_animating(self): 
        self.animating = False
        self.frames = 0  

    def draw(self, surf): 
        self.draw_fn(self, surf)

class PosMover(Mover): 
    def __init__(self, pos, draw_fn, easing_fn, animation_frames=60): 
        super().__init__(draw_fn, easing_fn, animation_frames)
        self.pos = pos 
        self.target = None 
        self.animating_start_pos = None

    def update(self): 
        if self.animating: 
            y = self.get_easing_value()
            self.pos = (
                (self.target[0] - self.animating_start_pos[0]) * y + self.animating_start_pos[0], 
                (self.target[1] - self.animating_start_pos[1]) * y + self.animating_start_pos[1]
            ) 
        super().update()

    def start_animating(self, target):
        super().start_animating()
        self.target = target 
        self.animating_start_pos = self.pos  

    def stop_animating(self):
        super().stop_animating()
        self.target = None 
        self.animating_start_pos = None 
    
class Animation: 
    current_sprite_idx: int | None
    frame_counter: int | None

    def __init__(self, sprites=None): 
        # holds tuples of (sprite surface, frame limit for this sprite)
        self.sprites = []
        if sprites is not None: 
            self.sprites = sprites 

        self.current_sprite_idx = None
        self.frame_counter = None

    def play(self): 
        self.current_sprite_idx = 0 
        self.frame_counter = 0  

    def cancel(self): 
        self.current_sprite_idx = None 
        self.frame_counter = None   

    def toggle(self): 
        if self.current_sprite_idx is None: 
            self.play() 
        else: 
            self.cancel()

    def update(self): 
        if self.current_sprite_idx is None or self.frame_counter is None: 
            return 

        # increment frame counter and check if sprite idx needs to be incremented
        _, frame_limit = self.sprites[self.current_sprite_idx]
        self.frame_counter += 1 
        if self.frame_counter >= frame_limit: 
            self.current_sprite_idx += 1
            self.frame_counter = 0

        # reset vars and return if animation has finished
        if self.current_sprite_idx >= len(self.sprites): 
            self.frame_counter = None 
            self.current_sprite_idx = None  

    def get_current_sprite(self): 
        if self.current_sprite_idx is None: 
            return None 
        
        return self.sprites[self.current_sprite_idx][0]
