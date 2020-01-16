# not used yet
import random
from particle import Particle

class Emitter:
    def __init__(self):
        pass

    def create_particles(self, position):
        particle_count = 10
        possible_velocity = range(-5, 6)
        for i in range(particle_count):
            Particle(position, random.choice(possible_velocity), random.choice(possible_velocity))
