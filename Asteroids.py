from SpaceObject import SpaceObject
import numpy as np


class Asteroids(SpaceObject):
    def __init__(self, biom, position, size, name, center=None, amount=175, size_range=(1,7), scale_factor=0.025):
        super().__init__(position, size, biom[0], f"{name} {biom[0]} asteroids")
        self.type = biom[-1]
        self.amount = amount
        self.centered = center
        self.angle = None
        self.size_range = size_range
        self.asteroid_scale_factor = scale_factor

    def calculate_asteroid_bounds(self, position, calculated_size, factor):
        return position - calculated_size * factor, position + calculated_size * factor

    def draw_asteroid(self, factor, canvas, angle):
        self.angle = angle
        self.draw(factor, canvas)

    def draw(self, factor, canvas):
        corr, ccorr = 3, 30
        correction_modes = (-1, 0, 1)
        for i in correction_modes:
            asteroid_positions = np.random.uniform(low=self.angle[0], high=self.angle[1], size=self.amount)
            for t in asteroid_positions:
                tmp = np.random.randint(low=self.size_range[0], high=self.size_range[1])
                asteroid_size = np.array((tmp, tmp))
                asteroid_factor = factor + i * self.asteroid_scale_factor
                asteroid_position = np.array((self.position[0] * np.cos(t), self.position[1] * np.sin(t))) * asteroid_factor + self.size
                lu, rb = self.calculate_asteroid_bounds(asteroid_position, asteroid_size, factor)
                canvas.ellipse((lu[0], lu[1], rb[0], rb[1]),
                               fill=tuple(self.color - np.array((i * ccorr, i * ccorr, i * ccorr))))

