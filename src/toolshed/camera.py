
class Camera: 
    def __init__(self, screen_dims, world_dims, camera_pos=(0,0)): 
        self.pos = camera_pos 
        self.dims = screen_dims
        self.world_dims = world_dims

    # get the position on screen for an entity that has a world position ...
    # it may be off screen based on the position of the entity vs the position of the camera
    def get_screen_pos(self, world_pos): 
        return world_pos[0] - self.pos[0], world_pos[1] - self.pos[1]

    # move camera to be centered on a certain world position
    def center_on(self, pos): 
        w, h = self.dims
        self.pos = (pos[0] - w//2, pos[1] - h//2)
        self.clamp()

    # do not allow camera to clip out of world bounds
    def clamp(self): 
        x, y = self.pos 
        w, h = self.world_dims
        x = max(x, 0)
        x = min(x, w - self.dims[0])
        y = max(y, 0)
        y = min(y, h - self.dims[1])
        self.pos = (x, y)