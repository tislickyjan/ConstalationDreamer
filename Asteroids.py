from SpaceObject import SpaceObject
import numpy as np


class Asteroids(SpaceObject):
    def __init__(self, color, position, size, name, amount=175):
        super().__init__(position, size, color, name)
        self.amount = amount
        self.angle = None

    def calculate_asteroid_bounds(self, position, calculated_size, factor):
        return position - calculated_size * factor, position + calculated_size * factor

    def draw_asteroid(self, factor, canvas, angle):
        self.angle = angle
        self.draw(factor, canvas)

    def draw(self, factor, canvas):
        corr, ccorr = 12, 30
        correction_modes = (-1, 0, 1)
        for i in correction_modes:
            asteroid_positions = np.random.uniform(low=self.angle[0], high=self.angle[1], size=self.amount)
            for t in asteroid_positions:
                tmp = np.random.randint(low=1, high=7)
                asteroid_size = np.array((tmp, tmp))
                asteroid_position = np.array((self.position[0] * np.cos(t), self.position[1] * np.sin(t))) * factor + self.size
                direction = asteroid_position - np.array(canvas.im.size) / 2
                asteroid_position += i * corr * (direction / np.linalg.norm(direction))
                # lu, rb = astPosition - asteroid_size, astPosition + asteroid_size
                lu, rb = self.calculate_asteroid_bounds(asteroid_position, asteroid_size, factor)
                canvas.ellipse((lu[0], lu[1], rb[0], rb[1]),
                               fill=tuple(self.color[-1] - np.array((i * ccorr, i * ccorr, i * ccorr))))

