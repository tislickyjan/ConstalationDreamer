from PIL import Image, ImageDraw
import numpy as np
from Asteroids import Asteroids


class ConstalationDrawer:
    final_image = None

    def __init__(self, storage):
        self.info_storage = storage
        self.image_size = np.array((1920 * 2, 1080 * 2)) # FULLHD
        # self.imageSize = np.array((7680*2,4320*2)) # 8K
        self.image_center = self.image_size / 2
        self.final_image = Image.new("RGBA", tuple(self.image_size), (0, 0, 0))
        self.draw_place = ImageDraw.Draw(self.final_image, 'RGBA')
        # self.multFac = 4 # 1 pro fullHD
        self.multiplicative_factor = 1.6 # 8 pro 8K, funguje jako zoom

    def get_factor(self):
        return self.multiplicative_factor

    def calculate_bounds(self, pos, size):
        return pos - np.array(size) * self.multiplicative_factor, pos + np.array(size) * self.multiplicative_factor

    def draw_sun_orbital(self, pos, size, angle):
        a, b = self.calculate_bounds(pos, size)
        orbital_color = (60, 60, 60)
        self.draw_place.arc((a[0], a[1], b[0], b[1]), start=np.rad2deg(angle[0]), end=np.rad2deg(angle[1]),
                            fill=orbital_color, width=3)

    def draw_star_system(self):
        self.sun_orbital_planets((np.pi, np.pi * 2),
                                 list(reversed(self.info_storage.planets)))

        for sun in self.info_storage.suns:
            sun.draw(self.multiplicative_factor, self.final_image)

        self.sun_orbital_planets((0, np.pi),
                                 self.info_storage.planets)

    def sun_orbital_planets(self, angle, space_objects):
        for space_object in space_objects:
            idx = self.info_storage.planets.index(space_object)
            if not isinstance(space_object, Asteroids):
                position = self.image_center + self.info_storage.random_position[idx]
                self.draw_sun_orbital(position, self.info_storage.return_size(idx), angle)
            if isinstance(space_object, Asteroids):
                space_object.draw_asteroid(self.multiplicative_factor, self.draw_place, angle)
            elif angle[0] <= space_object.t <= angle[1]:
                space_object.draw(self.multiplicative_factor, self.final_image)

    def draw_background(self):
        for star in self.info_storage.distant_stars:
            star.draw(self.multiplicative_factor, self.final_image)

    def clear_whole_image(self):
        self.final_image = Image.new("RGBA", tuple(self.image_size), (0, 0, 0))
        self.draw_place = ImageDraw.Draw(self.final_image, 'RGBA')