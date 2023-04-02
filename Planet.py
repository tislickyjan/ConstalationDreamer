from SpaceObject import SpaceObject
import numpy as np
from PIL import Image, ImageDraw


class Planet(SpaceObject):
    def __init__(self, name, surface, bbox, position, shift, size, t, rings=None, moons=None):
        self.box = bbox
        self.t = t
        self.rings = rings
        self.moons = moons
        self.shift = shift
        super().__init__(position, size, surface, name)

    def calculate_planet_bounds(self, position, factor):
        return position - self.size * factor, position + self.size * factor

    # TODO: předělat všude metodu draw, ktera bude brat navic parametr kreslici plochy, kam se vykresli obrazek, tim zustane kontrola nad velikosti kreslitka v režii draw modulu
    def draw(self, factor, canvas):
        # auxiliary_image = Image.new("RGBA", (512, 512), (120, 120, 120, 255))
        local_draw = ImageDraw.Draw(canvas)
        self.surface.generate_environment()
        # spravna pozice dle skalovani
        planet_true_pos = self.position * factor + self.shift
        pa, pb = self.calculate_planet_bounds(planet_true_pos, factor)
        planet_image = self.surface.final_image
        planet_image = planet_image.resize(tuple((pb - pa).astype(int)), resample=Image.LANCZOS)
        if self.rings is not None:
            # print("Adding antonov ring to planet {}".format(self.planets.index(planet)))
            self.rings.draw_asteroid(factor, local_draw, (np.pi, np.pi*2))
            canvas.alpha_composite(planet_image, tuple(pa.astype(int)))
            #canvas.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=self.surface[0], outline=self.outline)
            self.rings.draw_asteroid(factor, local_draw, (0, np.pi))
        else:
            canvas.alpha_composite(planet_image, tuple(pa.astype(int)))
            #canvas.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=self.surface[0])
        if self.moons is not None:
            t = np.random.uniform(low=0.0, high=2 * np.pi)
            moon_size, ring_size = 5, 10
            moon_factor = np.array((1.75, 1.75)) * self.size
            moon_position = np.array((np.cos(t), np.sin(t))) * moon_factor + planet_true_pos
            lu, rb = moon_position - moon_size * factor, moon_position + moon_size * factor
            # lu, rb = self.calculate_bounds(moon_position, moon_size)
            local_draw.ellipse((lu[0], lu[1], rb[0], rb[1]), fill=self.moons[0], outline=self.outline)
        # canvas.alpha_composite(auxiliary_image, tuple(pa.astype(int)))
