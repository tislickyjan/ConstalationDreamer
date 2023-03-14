from SpaceObject import SpaceObject
import numpy as np


class Sun(SpaceObject):
    def __init__(self, position, size, color, name):
        super().__init__(position, size, color, name)

    def draw(self, factor, canvas):
        a, b = self.calculate_bounds(factor)
        outline = tuple(np.clip(self.color[-1] + np.array((100, -50, -30)), 0, 255))
        canvas.ellipse((a[0], a[1], b[0], b[1]), outline=outline, fill=tuple(self.color[-1]), width=3)
