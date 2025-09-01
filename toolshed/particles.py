import pygame as pg 

from .vector import Vector

class ParticleManager: 
    def __init__(self): 
        self.particles = []

    def add_particle(self, p): 
        self.particles.append(p)

    def draw(self, surf): 
        for p in self.particles: 
            p.draw(surf)

    def update(self): 
        for p in self.particles: 
            p.update() 

        self.particles = list(filter(lambda x: x.alive, self.particles))

    def clear(self): 
        self.particles = []


class Particle: 
    # ID is used to tie particle to some kind of object 
    id = None 

    def __init__(self, pos: Vector, vel: Vector, timer: int): 
        self.pos = pos 
        self.vel = vel
        self.timer = timer
        self.alive = True 

    def __repr__(self): 
        return f'Particle(pos=({self.pos.x, self.pos.y})  alive={self.alive})'

    def update(self): 
        if not self.alive: 
            return 

        self.pos.add(self.vel)
        self.timer -= 1
        self.alive = self.timer > 0

        # TODO 
        # rotational veloctiy 
        # growing/shrinking 

    def kill(self): 
        self.alive = False 


class RectParticle(Particle): 
    def __init__(self, dim: Vector, pos: Vector, vel: Vector, timer: int): 
        super().__init__(pos, vel, timer) 
        self.dim = dim 

    def draw(self, surf): 
        x, y = self.pos.unpack()
        w, h = self.dim.unpack()
        r = pg.Rect(x, y, w, h)
        pg.draw.rect(surf, (0,0,0), r)


class CircParticle(Particle): 
    def __init__(self, rad: float, pos: Vector, vel: Vector, timer: int): 
        super().__init__(pos, vel, timer) 
        self.rad = rad 

    def draw(self, surf): 
        pg.draw.circle(surf, (0,0,0), self.pos.unpack(), self.rad) 

class CircGravityParticle(CircParticle): 
    def update(self):
        super().update()
        self.vel.y += .1

class PulseParticle(CircParticle): 
    def draw(self, surf): 
        pg.draw.circle(surf, (0,0,0), self.pos.unpack(), self.rad, width=1) 

    def update(self):
        super().update()
        self.rad += .3
