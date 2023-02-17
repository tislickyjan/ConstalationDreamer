from PIL import Image, ImageDraw
import numpy as np

class ConstalationDrawer:
    final_image = None

    def __init__(self):
        self.image_size = np.array((1920 * 2, 1080 * 2)) # FULLHD
        # self.imageSize = np.array((7680*2,4320*2)) # 8K
        self.final_image = Image.new("RGB", tuple(self.image_size))
        self.draw_place = ImageDraw.Draw(self.final_image, 'RGBA')
        # self.multFac = 4 # 1 pro fullHD
        self.multiplicative_factor = 1.6 # 8 pro 8K, funguje jako zoom

    def calculate_bounds(self, pos, size):
        return pos - np.array(size) * self.multiplicative_factor, pos + np.array(size) * self.multiplicative_factor

    def draw_sun(self, sun):
        a, b = self.calculate_bounds(sun.position, (sun.size, sun.size))
        outline = tuple(np.clip(sun.color + np.array((100,-50,-30)),0,255))
        self.draw_place.ellipse((a[0], a[1], b[0], b[1]), outline=outline, fill=sun.color, width=3)

    def draw_sun_orbital(self, pos, size, angle):
        a, b = self.calculate_bounds(pos, size)
        orbital_color = (60, 60, 60)
        self.draw_place.arc((a[0], a[1], b[0], b[1]), start=np.rad2deg(angle[0]), end=np.rad2deg(angle[1]), fill=orbital_color, width=3)

    def draw_planet(self, planet):
        t = np.random.uniform(low=0.0, high=2*np.pi)
        moon_size, ring_size = 5, 10
        # spravna pozice dle skalovani
        planet_true_pos = planet.position * self.multiplicative_factor + planet.shift
        pa,pb = self.calculate_bounds(planet_true_pos, planet.size)
        if planet.rings is not None:
            #print("Adding antonov ring to planet {}".format(self.planets.index(planet)))
            scaleFactor = (2,0.67)
            # a, b = planet.position - planet.size*scaleFactor, planet.position + planet.size*scaleFactor
            a, b = self.calculate_bounds(planet_true_pos, planet.size * scaleFactor)
            self.draw_place.arc((a[0], a[1], b[0], b[1]), start=180, end=360, fill=planet.rings[0], width=ring_size)
            self.draw_place.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=planet.color[0])
            self.draw_place.arc((a[0], a[1], b[0], b[1]), start=0, end=180, fill=planet.rings[0], width=ring_size)
        else:
            self.draw_place.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=planet.color[0])
        if planet.moons is not None:
            moon_factor = np.array((1.75,1.75))*planet.size
            moon_position = np.array((np.cos(t),np.sin(t)))*moon_factor + planet_true_pos
            # lu,rb = moonPosition - moon_size, moonPosition + moon_size
            lu,rb = self.calculate_bounds(moon_position, moon_size)
            self.draw_place.ellipse((lu[0], lu[1], rb[0], rb[1]), fill=planet.moons[0])

    def draw_asteroid_field(self, field, angle):
        #print(f"Asteroids on position {self.planets.index(field)}")
        amount = 175
        corr, ccorr = 12, 30
        correction_modes = (-1,0,1)
        for i in correction_modes:
            asteroid_positions = np.random.uniform(low=angle[0],high=angle[1],size=amount)
            for t in asteroid_positions:
                tmp = np.random.randint(low=1,high=7)
                asteroid_size = np.array((tmp,tmp))
                asteroid_position = np.array((field.position[0] * np.cos(t), field.position[1] * np.sin(t))) * \
                              self.multiplicative_factor + field.size
                direction = asteroid_position - self.image_size / 2
                asteroid_position += i*corr*(direction/np.linalg.norm(direction))
                # lu, rb = astPosition - asteroid_size, astPosition + asteroid_size
                lu, rb = self.calculate_bounds(asteroid_position, asteroid_size)
                self.draw_place.ellipse((lu[0], lu[1], rb[0], rb[1]),
                                        fill=tuple(field.color[-1]-np.array((i*ccorr, i*ccorr, i*ccorr))))