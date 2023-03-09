from PIL import Image
import numpy as np
import Draw
import ConstalationParser as conPar
import GeneralInformation as genStorage
from Sun import Sun
from Asteroids import Asteroids
from Planet import Planet
from pathlib import Path


# vypocítava celou vyslednou soustavu na zaklade parametru, pripadne upravuje vysledek
class ConstalationDreamer:
    final_image = None
    draw_tool = None

    def __init__(self):
        self.information_storage = genStorage.GeneralStorage()
        self.draw_tool = Draw.ConstalationDrawer(self.information_storage)
        self.parsed_info = conPar.ConstalationParser(self.information_storage)
        # tato cast musi jit pozdeji jinam, hlavne kdyz budu chtit vystavit na web jako jednu z komponent

    def dream(self, text):
        self.parsed_info.init(text)

        self.generate_space_environment()

        self.draw_tool.draw_background()

        self.draw_tool.draw_star_system()

    def generate_space_environment(self):
        self.parsed_info.read_distant_stars(self.draw_tool.image_size)
        for i in range(self.information_storage.number_of_suns):
            position = self.draw_tool.image_center + np.array((np.random.randint(low=-200, high=200),
                                                               np.random.randint(low=-20, high=20)))
            local_sun = self.parsed_info.read_sun_info(i)
            self.information_storage.suns.append(Sun(position, local_sun["size"], local_sun["color"], local_sun["name"]))
        for i in range(self.information_storage.number_of_planets):
            position = self.draw_tool.image_center + self.information_storage.random_position[i]
            size = self.information_storage.return_size(i)
            space_object = self.parsed_info.read_object_info(i)
            if space_object["size"] is None:
                self.asteroid_field(position, size, space_object)
            else:
                self.place_planet(position, size, space_object)

    def place_planet(self, pos, size, obj):
        t = np.random.uniform(low=0.0,high=2*np.pi)
        planet_position = np.array((size[0]*np.cos(t),size[1]*np.sin(t)))
        planet_size = np.array((obj["size"],obj["size"]))
        lu, rb = planet_position - planet_size, planet_position + planet_size
        astpos = planet_position * self.draw_tool.get_factor() + pos
        astsize = planet_size * np.array((2, 0.67))
        rings = Asteroids(obj["asteroids"], astsize, astpos, obj['name'],
                          planet_position, 100, (1,3), 0.2) if obj["asteroids"] else None
        self.information_storage.planets.append(Planet(obj["name"], obj["biom"],(lu[0], lu[1], rb[0], rb[1]),
                                                       planet_position, pos, planet_size, t,
                                                       rings=rings,
                                                       moons=obj["moons"]))

    def asteroid_field(self, pos, size, obj):
        self.information_storage.planets.append(Asteroids(obj["biom"], size, pos, obj["name"]))

    #TODO: Nebula effect in system
    # def add_nebula(self):
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
    for i in ["Jan Tislický"]:
        print(f"dreaming about {i}")
        cdreamer.dream(i)
        cdreamer.final_image = cdreamer.draw_tool.final_image.resize(cdreamer.draw_tool.image_size // 2,
                                                                     resample=Image.LANCZOS)
        cdreamer.final_image.show()
        # cdreamer.final_image.save(Path(f"./examples/star_system_{'_'.join(i.split(' '))}.png"))
        print(f"finished {i}")
        print("-"*50)
        print()
        cdreamer.information_storage.clear_all_info()
        cdreamer.draw_tool.clear_whole_image()

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