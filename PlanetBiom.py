import numpy as np
import opensimplex
from PIL import Image

# TODO: optimise with NUMBA once its released
class PlanetBiotops:

    def __init__(self, seed, name, colors):
        self.seed = seed
        self.biom_name = name
        self.colors = colors
        self.terrain = np.zeros((2048, 2048))
        self.moisture = np.zeros((2048, 2048))
        self.final_image = Image.new("RGBA", (1024, 1024))
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
        amplify = np.vectorize(lambda element: element * 1.15 if element > 0.339 else element)
        make_mask = np.vectorize(lambda element: 1 if element > 0.339 else 0)
        self.filter = amplify(self.filter)
        self.mask = make_mask(self.filter)
        self.filter /= self.filter.max()

    @staticmethod
    def noise(nx, ny):
        return opensimplex.noise2(nx, ny) / 2.0 + 0.5

    def generate_terrain(self):
        opensimplex.seed(self.seed)
        for y in range(self.terrain.shape[0]):
            for x in range(self.terrain.shape[1]):
                nx, ny = x/self.terrain.shape[1] - 0.5, y/self.terrain.shape[1] - 0.5
                elevation = 0.125*self.noise(8*nx + 2.35, 8*ny + 5.21) + \
                            0.0625*self.noise(16*nx, 16*ny + 5.87) + \
                            0.03125*self.noise(32*nx, 32*ny) + \
                            0.015625*self.noise(64*nx, 64*ny)
                self.terrain[y,x] = elevation / (0.125+0.0625+0.03125+0.015625)

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

        # img = Image.fromarray(np.uint8(self.mask * 255))
        # img.show()

    def fill_final_image(self):
        for y in range(self.terrain.shape[0]):
            for x in range(self.terrain.shape[0]):
                ...

    def generate_environment(self, seed, name):
        self.generate_terrain()
        # self.generate_moisture()
        self.filter_textures()
        self.fill_final_image()


if __name__ == "__main__":
    biom = PlanetBiotops(658731, 2, [(5, 142, 217), (242, 208, 169), (82, 151, 53), (5, 59, 6), (72, 74, 71)])
    # biom.generate_moisture()
    # biom.generate_terrain()
    biom.filter_textures()