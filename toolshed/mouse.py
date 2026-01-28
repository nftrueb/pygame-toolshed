import pygame as pg 
from .window import PygameContext
from .particles import ParticleManager, PulseParticle
from .vector import Vector

class Mouse: 
    def __init__(self, 
                 color=(50,50,50), 
                 rad=8, 
                 weight=2, 
                 click_particles=True, 
                 trail_particles=False, 
                 mouse_pressed_event_handler=None): 
        self.x, self.y = 0, 0
        self.color = color 
        self.rad = rad 
        self.weight = weight
        self.click_particles = click_particles
        self.trail_particles = trail_particles
        self.mouse_pressed_event_handler = mouse_pressed_event_handler
        self.pressed = False

        self.timer = 15

        pg.mouse.set_visible(False)

    def pos(self): 
        return self.x, self.y

    def draw(self, surf): 
        w = 0 if self.pressed else self.weight
        pg.draw.circle(surf, self.color, self.pos(), self.rad, w)

    def update(self, pc: PygameContext): 
        self.x, self.y = pc.get_event_context().mouse_pos

    def handle_event(self, event: pg.Event, pm: ParticleManager | None = None ): 
        rad = self.rad 
        make_particle = False 
        if event.type == pg.MOUSEBUTTONDOWN: 
            self.pressed = True 
            if self.mouse_pressed_event_handler is not None: 
                self.mouse_pressed_event_handler(self)

            make_particle = self.click_particles

        elif event.type == pg.MOUSEBUTTONUP: 
            self.pressed = False
            make_particle = self.click_particles

        elif event.type in { pg.MOUSEMOTION, pg.MOUSEWHEEL }: 
            rad *= 0.5
            make_particle = self.trail_particles

        if make_particle: 
            if pm is not None: 
                pm.add_particle(
                    PulseParticle(
                        Vector(self.x, self.y), 
                        Vector(0,0), 
                        self.timer, 
                        color=self.color, 
                        rad = rad
                    )
                )
            else: 
                logger.info('Indicated mouse to create particles but did not provide ParticleManager') 
