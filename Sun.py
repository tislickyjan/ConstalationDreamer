from SpaceObject import SpaceObject
from PIL import Image
import numpy as np


class Sun(SpaceObject):
    def __init__(self, position, size, surface, name):
        super().__init__(position, size, surface, name)

    def draw(self, factor, image):
        self.surface.generate_environment()
        a, b = self.calculate_bounds(factor)
        sun_image = self.surface.final_image.resize(tuple((b-a).astype(int)), resample=Image.LANCZOS)
        image.alpha_composite(sun_image, tuple(a.astype(int)))
        # outline = tuple(np.clip(self.surface.colors[-1] + np.array((100, -50, -30)), 0, 255))
        # canvas.ellipse((a[0], a[1], b[0], b[1]), outline=outline, fill=tuple(self.surface.colors[-1]), width=3)
