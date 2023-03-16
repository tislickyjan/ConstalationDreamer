import numpy as np
import opensimplex
from PIL import Image
# from pathlib import Path
# from ConstalationParser import ConstalationParser
# from GeneralInformation import GeneralStorage


# TODO: optimise with NUMBA once its released
class ObjectEnvironment:

    def __init__(self, seed, name, colors):
        self.seed = seed
        self.biom_name = name
        self.colors = colors
        self.noise_exponents = np.array((0.125, 0.0625, 0.03125, 0.015625))
        self.terrain = np.zeros((512, 512))
        self.moisture = np.zeros((512, 512))
        self.final_image = Image.new("RGBA", (512, 512))
        self.filter = np.zeros(tuple(self.terrain.shape))
        self.mask = np.zeros(tuple(self.terrain.shape))
        self.create_filter()

    def set_default_noise_exponents(self):
        self.noise_exponents = np.array((0.125, 0.0625, 0.03125, 0.015625))

    def set_noise_exponents(self, exponents):
        self.noise_exponents = exponents

    def create_filter(self):
        center = np.array(self.terrain.shape) // 2
        for y in range(self.filter.shape[0]):
            for x in range(self.filter.shape[1]):
                distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
                self.filter[y, x] = distance / (np.sqrt(2) * center[0])

        self.filter = 1 - self.filter
        amplify = np.vectorize(lambda element: element * 1.18 if element > 0.339 else element)
        make_mask = np.vectorize(lambda element: 1 if element > 0.339 else 0)
        self.filter = amplify(self.filter)
        self.mask = make_mask(self.filter)
        self.filter /= self.filter.max()

    @staticmethod
    def noise(nx, ny):
        return opensimplex.noise2(nx, ny) / 2.0 + 0.5

    def get_noise_on_coordinates(self, x, y, shifts=None):
        if shifts is None:
            shifts = [0, 0, 0, 0, 0, 0, 0, 0]
        nx, ny = x / self.terrain.shape[1] - 0.5, y / self.terrain.shape[1] - 0.5
        value = self.noise_exponents[0] * self.noise(8 * nx + shifts[0], 8 * ny + shifts[1]) + \
                self.noise_exponents[1] * self.noise(16 * nx + shifts[2], 16 * ny + shifts[3]) + \
                self.noise_exponents[2] * self.noise(32 * nx + shifts[4], 32 * ny + shifts[5]) + \
                self.noise_exponents[3] * self.noise(64 * nx + shifts[6], 64 * ny + shifts[7])
        return value

    def generate_map_from_seed(self, seed, target, noise_shifts, value_exponent):
        opensimplex.seed(seed)
        for y in range(target.shape[0]):
            for x in range(target.shape[1]):
                target[y, x] = self.get_noise_on_coordinates(x, y, noise_shifts)
        target **= value_exponent
        target /= self.noise_exponents.sum()

    def filter_textures(self):
        self.terrain *= self.filter
        self.terrain = np.uint8(np.round(self.terrain * 255))
        self.moisture *= self.filter
        self.moisture = np.uint8(np.round(self.moisture * 255))

    def fill_final_image(self, modifier):
        color = np.array((0, 0, 0))
        for y in range(self.terrain.shape[0]):
            for x in range(self.terrain.shape[0]):
                if self.terrain[y, x] < (14 + modifier):  # really deep OCEAN
                    color = self.colors[0] * 0.25
                elif self.terrain[y, x] < (19 + modifier):  # deep OCEAN
                    color = self.colors[0] * 0.5
                elif self.terrain[y, x] < (20 + modifier):  # ocean
                    color = self.colors[0]
                elif self.terrain[y, x] < (21 + modifier):  # BEACH
                    color = self.colors[1] * 0.9

                # hory
                elif self.terrain[y, x] > (43 + modifier):
                    if self.moisture[y, x] < 97:  # SCORCHED
                        color = self.colors[4] * 0.8
                    elif self.moisture[y, x] < 135:  # BARE
                        color = self.colors[4] * 1.4
                    elif self.moisture[y, x] < 153:  # TUNDRA
                        color = self.colors[5] * 0.9
                    else:  # snow
                        color = self.colors[5]

                elif self.terrain[y, x] > (36 + modifier):
                    if self.moisture[y, x] < 84:  # TEMPERATE_DESERT
                        color = self.colors[2] * 0.8
                    elif self.moisture[y, x] < 168:  # SHRUBLAND
                        color = self.colors[3] * 1.25
                    else:   # TAIGA
                        color = self.colors[3] * 1.68

                elif self.terrain[y, x] > (25 + modifier):
                    if self.moisture[y, x] < 24:  # TEMPERATE_DESERT
                        color = self.colors[2] * 0.8
                    elif self.moisture[y, x] < 80:  # GRASSLAND
                        color = self.colors[2] * 1.2
                    elif self.moisture[y, x] < 212:  # TEMPERATE_DECIDUOUS_FOREST
                        color = self.colors[2] * 0.628
                    else:  # TEMPERATE_RAIN_FOREST
                        color = self.colors[3]

                else:
                    if self.moisture[y, x] < 61:  # SUBTROPICAL_DESERT
                        color = self.colors[1] * 1.13
                    elif self.moisture[y, x] < 97:  # GRASSLAND
                        color = self.colors[2] * 1.2
                    elif self.moisture[y, x] < 175:  # TROPICAL_SEASONAL_FOREST
                        color = self.colors[2] * 0.84
                    else:  # TROPICAL_RAIN_FOREST
                        color = self.colors[2] * 0.823
                self.final_image.putpixel((x, y), (*np.uint8(np.round(np.clip(color, 0, 255))),
                                                   np.uint8(np.round(self.mask[y, x] * 255))))

    # seed a name v hlavicce?
    def generate_environment(self):
        self.generate_map_from_seed(self.seed, self.terrain, [2.35, 5.21, 0, 5.87, 0, 0, 0, 0], 1.638)
        self.generate_map_from_seed(self.seed ** 2, self.moisture, [3.89, 2.15, 0, 0, 10.658, 0, 0, 18.3], 1)
        self.filter_textures()
        value = self.seed % 23
        elevation_modifier = value if self.biom_name == "ocean" else value // 2 if self.biom_name == "terran" else -value
        self.fill_final_image(elevation_modifier)


if __name__ == "__main__":
    ...
    # info = GeneralStorage()
    # parser = ConstalationParser(info)
    # 658731, 1, 1000, 3684
    # for i in ["Jan Tislický"]:
    #     parser.init(i)
        # biom = ObjectEnvironment(parser.get_object(2), "terran", parser.return_object_colors(2))
        # biom = ObjectEnvironment(parser.get_sun(1), "", parser.read_sun_colors(1))
        # biom.set_noise_exponents(np.array((0, 0, 0.03125, 0.015625)))
        # biom.generate_environment()
        # biom.final_image.show()
        # biom.final_image.save(Path(f"./examples/biom_generator_{i}.png"))
        # print(f"biom number {i} saved")
        #[np.array((5, 142, 217)), np.array((242, 208, 169)),np.array((82, 151, 53)), np.array((5, 59, 6)), np.array((72, 74, 71))]
