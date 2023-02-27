import numpy as np
import noise

scale = 100
octaves = 6
persistance = 0.5
lacunarity = 1.9


def generate(size):
    surface = [[0.0 for i in range(size)] for j in range(size)]
    for y in range(size):
        for x in range(size):
            surface[x][y] = noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistance,
                                          lacunarity=lacunarity, repeatx=size, repeaty=size, base=0)
    return surface

def generateImg(img, size):
    for y in range(size):
        for x in range(size):
            value = noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistance, lacunarity=lacunarity,
                                  repeatx=size, repeaty=size, base=0)
            img.putpixel((x,y), int(np.interp(value, [-1, 1], [0, 255])))
