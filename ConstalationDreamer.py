from PIL import Image
import numpy as np
import Draw
import ConstalationParser as conPar
from Sun import Sun
from Asteroids import Asteroids
from Planet import Planet


# vypocítava celou vyslednou soustavu na zaklade parametru, pripadne upravuje vysledek
class ConstalationDreamer:
    final_image = None
    draw_tool = None
    planets = []
    suns = []
    orbA = 0
    orbB = 0
    step = 0

    def __init__(self):
        self.number_of_planets = 10
        self.number_of_suns = 1
        self.draw_tool = Draw.ConstalationDrawer()
        self.parsed_info = conPar.ConstalationParser()
        self.parsed_info.Init("Jan Tislický")

    def Dream(self):
        # nacti potrebne informace
        self.orbA, self.orbB, self.step = self.parsed_info.read_general_info()
        self.number_of_suns, self.number_of_planets = \
            self.parsed_info.read_suns_count(), self.parsed_info.read_objects_count()
        # random displace for palnets and orbitals, asteroids...
        rand_position = np.random.randint(low=-15, high=15, size=self.number_of_planets)
        self.generate_space_environment(rand_position)

        self.sun_orbital_planets(rand_position, (np.pi, np.pi * 2), (self.number_of_planets - 1, -1, -1))

        for i in range(self.number_of_suns):
            self.draw_tool.draw_sun(self.suns[i])

        self.sun_orbital_planets(rand_position, (0, np.pi), (0, self.number_of_planets, 1))

    def generate_space_environment(self, rand_transform):
        for i in range(self.number_of_suns):
            position = self.draw_tool.image_size / 2 + np.array((np.random.randint(low=-200, high=200),
                                                                 np.random.randint(low=-20, high=20)))
            local_sun = self.parsed_info.read_sun_info(i)
            self.suns.append(Sun(position, local_sun["size"], local_sun["color"], local_sun["name"]))
        for i in range(self.number_of_planets):
            position = self.draw_tool.image_size / 2 + rand_transform[i]
            size = (self.orbA + i * self.step, self.orbB + i * self.step // 3)
            space_object = self.parsed_info.read_object_info(i)
            if space_object["size"] is None:
                self.asteroid_field(position, size, space_object)
            else:
                self.place_planet(position, size, space_object)

    def sun_orbital_planets(self, rand_trans, angle, iterator_range):
        for i in range(iterator_range[0], iterator_range[1], iterator_range[2]):
            if not isinstance(self.planets[i], Asteroids):
                position = self.draw_tool.image_size / 2 + rand_trans[i]
                self.draw_tool.draw_sun_orbital(position, (self.orbA + i * self.step, self.orbB + i * self.step // 3), angle)
            if isinstance(self.planets[i], Asteroids):
                self.draw_tool.draw_asteroid_field(self.planets[i], angle)
            elif angle[0] <= self.planets[i].t <= angle[1]:
                self.draw_tool.draw_planet(self.planets[i])

    def place_planet(self, pos, size, obj):
        t = np.random.uniform(low=0.0,high=2*np.pi)
        planet_position = np.array((size[0]*np.cos(t),size[1]*np.sin(t)))
        planet_size = np.array((obj["size"],obj["size"]))
        lu, rb = planet_position - planet_size, planet_position + planet_size
        self.planets.append(Planet(obj["name"], obj["biom"],(lu[0], lu[1], rb[0], rb[1]), planet_position, pos,
                                   planet_size, t, rings=obj["asteroids"], moons=obj["moons"]))

    def asteroid_field(self, pos, size, obj):
        self.planets.append(Asteroids(obj["biom"], size, pos, obj["name"]))

    #TODO: Nebula effect in system
    # def add_nebula(self):
    #     ...

    #TODO: Background stars
    # def background_stars(self):
    #     ...

    #TODO: Megastructures
    # def megastructures(self):
    #    ...

    #TODO: Fauna and flora
    # def biomes(self):
    #    ...

    #TODO: nice to have - vsechny planety budou videt a zadna nebude za sluncem plus rovznomerne rozlozeni


if __name__ == "__main__":
    cdreamer = ConstalationDreamer()
    cdreamer.Dream()
    cdreamer.final_image = cdreamer.draw_tool.final_image.resize(cdreamer.draw_tool.image_size // 2,
                                                                 resample=Image.LANCZOS)
    cdreamer.final_image.show()

    """
        rotovani planet
        tmpRotPl = Image.new("RGBA", (80,40))
        imgSize = np.array(tmpRotPl.size)
        draw = ImageDraw.Draw(tmpRotPl)
        a, b = planet[1] - planet[2]*scaleFactor, planet[1] + planet[2]*scaleFactor
        draw.arc((0, 10, 80, 30), start=180, end=360, fill=(255,0,0), width=ringSize)
        draw.ellipse((20,0,60,40), fill=color)
        draw.arc((0, 10, 80, 30), start=0, end=180, fill=(255,0,0), width=ringSize)
        rotated = tmpRotPl.rotate(0,expand=True)
        self.finalImage.paste(rotated,planet[0],rotated)
    """