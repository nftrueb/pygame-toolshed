from typing import Tuple
from dataclasses import dataclass

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


@dataclass
class Particle: 
    pos: Vector 
    vel: Vector
    timer: int 
    id: int | None = None
    color: Tuple[int] = (0,0,0)
    alive: bool = True

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

@dataclass
class RectParticle(Particle): 
    dim: Vector = None

    def draw(self, surf): 
        x, y = self.pos.unpack()
        w, h = self.dim.unpack()
        r = pg.Rect(x, y, w, h)
        pg.draw.rect(surf, self.color, r)

@dataclass
class CircParticle(Particle): 
    rad: int = 3

    def draw(self, surf): 
        pg.draw.circle(surf, self.color, self.pos.unpack(), self.rad) 

@dataclass
class CircGravityParticle(CircParticle): 
    def update(self):
        super().update()
        self.vel.y += .1

@dataclass
class PulseParticle(CircParticle): 
    def draw(self, surf): 
        pg.draw.circle(surf, self.color, self.pos.unpack(), self.rad, width=1) 

    def update(self):
        super().update()
        self.rad += .3
