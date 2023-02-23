import abc
import numpy as np


class SpaceObject(metaclass=abc.ABCMeta):
    def __init__(self, position, size, color, name=""):
        self.position = position
        self.size = size
        self.color = color
        self.name = name
        self.outline = (0, 0, 0)

    def calculate_bounds(self, factor):
        return self.position - np.array(self.size) * factor, self.position + np.array(self.size) * factor

    @abc.abstractmethod
    def draw(self, factor, canvas):
        pass
