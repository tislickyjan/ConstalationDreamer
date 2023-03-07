import numpy as np
import opensimplex
from PIL import Image

# TODO: optimise with NUMBA once its released
class PlanetBiotops:

    def __init__(self, seed, name, colors):
        self.seed = seed
        self.biom_name = name
        self.colors = colors
        self.terrain = np.zeros((512, 512))
        self.moisture = np.zeros((512, 512))
        self.final_image = Image.new("RGBA", (512, 512))
        self.filter = np.zeros(tuple(self.terrain.shape))
        self.mask = np.zeros(tuple(self.terrain.shape))
        self.create_filter()

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

    def generate_terrain(self):
        opensimplex.seed(self.seed)
        # exponent_1, exponent_2, exponent_3, exponent_4 = 0.125, 0.0625, 0.03125, 0.015625
        exponent_1, exponent_2, exponent_3, exponent_4 = 0.125, 0.0625, 0.03125, 0.015625
        for y in range(self.terrain.shape[0]):
            for x in range(self.terrain.shape[1]):
                nx, ny = x/self.terrain.shape[1] - 0.5, y/self.terrain.shape[1] - 0.5
                elevation = exponent_1*self.noise(8*nx + 2.35, 8*ny + 5.21) + \
                            exponent_2*self.noise(16*nx, 16*ny + 5.87) + \
                            exponent_3*self.noise(32*nx, 32*ny) + \
                            exponent_4*self.noise(64*nx, 64*ny)
                elevation = elevation ** 1.638
                self.terrain[y, x] = elevation / (exponent_1 + exponent_2 + exponent_3 + exponent_4)

    def generate_moisture(self):
        opensimplex.seed(self.seed ** 2)
        for y in range(self.moisture.shape[0]):
            for x in range(self.moisture.shape[1]):
                nx, ny = x / self.moisture.shape[1] - 0.5, y / self.moisture.shape[1] - 0.5
                moisture = 0.125 * self.noise(8 * nx + 3.89, 8 * ny + 2.15) + \
                            0.0625 * self.noise(16 * nx, 16 * ny) + \
                            0.03125 * self.noise(32 * nx + 10.658, 32 * ny) + \
                            0.015625 * self.noise(64 * nx, 64 * ny + 18.3)
                self.moisture[y,x] = moisture / (0.125 + 0.0625 + 0.03125 + 0.01562)

    def filter_textures(self):
        self.terrain *= self.filter
        self.moisture *= self.filter

        # img = Image.fromarray(np.uint8(self.terrain * 255))
        # img.show()
        # img = Image.fromarray(np.uint8(self.moisture * 255))
        # img.show()

    def fill_final_image(self):
        color = np.array((0, 0, 0))
        for y in range(self.terrain.shape[0]):
            for x in range(self.terrain.shape[0]):
                if self.terrain[y, x] < 0.055:  # really deep OCEAN
                    color = self.colors[0] * 0.25
                elif self.terrain[y, x] < 0.075:  # deep OCEAN
                    color = self.colors[0] * 0.5
                elif self.terrain[y, x] < 0.08:  # ocean
                    color = self.colors[0]
                elif self.terrain[y, x] < 0.081:  # BEACH
                    color = self.colors[1] * 0.9

                # hory
                elif self.terrain[y, x] > 0.17:
                    if self.moisture[y, x] < 0.38:  # SCORCHED
                        color = self.colors[4] * 0.8
                    elif self.moisture[y, x] < 0.53:  # BARE
                        color = np.clip(self.colors[4] * 1.4, 0, 255)
                    elif self.moisture[y, x] < 0.6:  # TUNDRA
                        color = np.array(np.uint8((235, 235, 235)))
                    else:  # snow
                        color = np.array(np.uint8((250, 250, 250)))

                elif self.terrain[y, x] > 0.14:
                    if self.moisture[y, x] < 0.33:  # TEMPERATE_DESERT
                        color = self.colors[2] * 0.8
                    elif self.moisture[y, x] < 0.66:  # SHRUBLAND
                        color = np.clip(self.colors[3] * 1.25, 0, 255)
                    else:   # TAIGA
                        color = np.clip(self.colors[3] * 1.68, 0, 255)

                elif self.terrain[y, x] > 0.1:
                    if self.moisture[y, x] < 0.096:  # TEMPERATE_DESERT
                        color = self.colors[2] * 0.8
                    elif self.moisture[y, x] < 0.316:  # GRASSLAND
                        color = np.clip(self.colors[2] * 1.2, 0, 255)
                    elif self.moisture[y, x] < 0.83:  # TEMPERATE_DECIDUOUS_FOREST
                        color = self.colors[2] * 0.628
                    else:  # TEMPERATE_RAIN_FOREST
                        color = self.colors[3]

                else:
                    if self.moisture[y, x] < 0.24:  # SUBTROPICAL_DESERT
                        color = np.clip(self.colors[1] * 1.13, 0, 255)
                    elif self.moisture[y, x] < 0.38:  # GRASSLAND
                        color = np.clip(self.colors[2] * 1.2, 0, 255)
                    elif self.moisture[y, x] < 0.69:  # TROPICAL_SEASONAL_FOREST
                        color = self.colors[2] * 0.84
                    else:  # TROPICAL_RAIN_FOREST
                        color = self.colors[2] * 0.823
                self.final_image.putpixel((x, y), (*np.uint8(np.round(color)), self.mask[y, x] * 255))

    # seed a name v hlavicce?
    def generate_environment(self):
        self.generate_terrain()
        self.generate_moisture()
        self.filter_textures()
        self.fill_final_image()


if __name__ == "__main__":
    biom = PlanetBiotops(99830217, 2, [np.array((5, 142, 217)), np.array((242, 208, 169)), np.array((82, 151, 53)),
                                     np.array((5, 59, 6)), np.array((72, 74, 71))])
    # 658731
    # biom.generate_moisture()
    # biom.generate_terrain()
    # biom.filter_textures()
    biom.generate_environment()
    biom.final_image.show()