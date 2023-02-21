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
        self.final_image = Image.new("RGB", tuple(self.image_size))
        self.draw_place = ImageDraw.Draw(self.final_image, 'RGBA')
        # self.multFac = 4 # 1 pro fullHD
        self.multiplicative_factor = 1.6 # 8 pro 8K, funguje jako zoom

    def calculate_bounds(self, pos, size):
        return pos - np.array(size) * self.multiplicative_factor, pos + np.array(size) * self.multiplicative_factor

    def draw_sun_orbital(self, pos, size, angle):
        a, b = self.calculate_bounds(pos, size)
        orbital_color = (60, 60, 60)
        self.draw_place.arc((a[0], a[1], b[0], b[1]), start=np.rad2deg(angle[0]), end=np.rad2deg(angle[1]),
                            fill=orbital_color, width=3)

    def draw_star_system(self):
        self.sun_orbital_planets(self.info_storage.random_position, (np.pi, np.pi * 2),
                                 (self.info_storage.number_of_planets - 1, -1, -1))

        for sun in self.info_storage.suns:
            sun.draw(self.multiplicative_factor, self.draw_place)

        self.sun_orbital_planets(self.info_storage.random_position, (0, np.pi),
                                 (0, self.info_storage.number_of_planets, 1))

    def sun_orbital_planets(self, rand_trans, angle, iterator_range):
        for i in range(iterator_range[0], iterator_range[1], iterator_range[2]):
            if not isinstance(self.info_storage.planets[i], Asteroids):
                position = self.image_center + rand_trans[i]
                self.draw_sun_orbital(position, self.info_storage.return_size(i), angle)
            if isinstance(self.info_storage.planets[i], Asteroids):
                self.info_storage.planets[i].draw_asteroid(self.multiplicative_factor, self.draw_place, angle)
            elif angle[0] <= self.info_storage.planets[i].t <= angle[1]:
                self.info_storage.planets[i].draw(self.multiplicative_factor, self.draw_place)