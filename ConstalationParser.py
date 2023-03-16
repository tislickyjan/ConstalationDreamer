from numpy import log as nlog, random, array as nparray, clip
from GeneralInformation import GeneralStorage
from DistantStars import DistantStar
from PlanetBiom import ObjectEnvironment


class ConstalationParser:
    original_string = None
    hexadecimal_representation = None
    hexadecimal_length = None
    maxCountObj = 11

    # slovnik s maskami jednotlivych casti, cislo na druhem miste udava pocet nul zprava
    masks = {
        "suns":     (int(0xf),49),
        "s0c":      (int(0xffff),45),
        "s1c":      (int(0xffff),43),
        "s2c":      (int(0xffff),40),
        "orba":     (int(0x4ff),37),
        "orbb":     (int(0x4ff),34),
        "step":     (int(0xfff),31),
        "distant_stars": (int(0xfffff),26),
        "objs":     (int(0xf),25),
        "obj0":     (int(0xff),23),
        "obj1":     (int(0xff),21),
        "obj2":     (int(0xff),19),
        "obj3":     (int(0xff),17),
        "obj4":     (int(0xff),15),
        "obj5":     (int(0xff),13),
        "obj6":     (int(0xff),11),
        "obj7":     (int(0xff),9),
        "obj8":     (int(0xff),7),
        "obj9":     (int(0xff),5),
        "obj10":    (int(0xff),3),
        "obj11":    (int(0xff),1),
    }

    color_masks = {
        "obj0":     [19, 17, 11, 27],
        "obj1":     [13, 25, 2, 38],
        "obj2":     [43, 31, 28, 12],
        "obj3":     [36, 0, 24, 42],
        "obj4":     [9, 35, 34, 37],
        "obj5":     [8, 16, 32, 26],
        "obj6":     [6, 5, 14, 29],
        "obj7":     [32, 22, 18, 3],
        "obj8":     [20, 10, 30, 40],
        "obj9":     [15, 23, 1, 4],
        "obj10":    [38, 33, 21, 7],
        "obj11":    [39, 41, 19, 8],
    }

    bioms = [
        (0,0,0), # asteroids
        (247, 70, 3), # lava
        (51, 102, 255), # ocean
        (102, 153, 0), # desert
        (128, 128, 128), # barren
        (0, 153, 51), # forrest
        (85, 128, 0), # terran
    ]

    biom_environment = [
        "asteroids",
        "lava",
        "ocean",
        "desert",
        "barren",
        "forrest",
        "terran",
    ]

    asteroids = [
        (75, 75, 75), (30, 144, 255), (205, 133, 63)
    ]

    astType = ["rocks", "ice", "metals&rocks"]

    def __init__(self, info):
        self.info_store = info

    def init(self, text):
        self.original_string = text
        try :
            self.hexadecimal_representation = int(self.original_string.encode('utf-8'), 16)
        except ValueError:
            self.hexadecimal_representation = int(self.original_string.encode('utf-8').hex(), 16)
        self.hexadecimal_length = len(hex(self.hexadecimal_representation)) - 2

        while self.hexadecimal_length < 50:
            self.hexadecimal_representation += int(hex(self.hexadecimal_representation ** 2 *
                                                       self.hexadecimal_length), 16)
            self.hexadecimal_length = len(hex(self.hexadecimal_representation)) - 2
        if self.hexadecimal_length > 50:
            self.hexadecimal_representation = int(str(hex(self.hexadecimal_representation))[:52], 16)
            self.hexadecimal_length = len(hex(self.hexadecimal_representation)) - 2
        # print(int(str(hex(self.hexRepre))[:50],16))
        # nastav sdilene informace
        self.info_store.set_general_information(self.read_general_info())
        self.info_store.set_number_of_objects(self.read_suns_count(), self.read_objects_count())
        # random displace for planets and orbitals, asteroids...
        self.info_store.set_rand_pos(random.randint(low=-15, high=15, size=self.info_store.number_of_planets))

    def mask_input(self, numerical_mask, offset):
        res = (self.hexadecimal_representation >> (offset * 4)) & numerical_mask
        return res

    # source: https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
    @staticmethod
    def kelvin_to_rgb(temp):
        # print(temp)
        if temp > 40000:
            temp = 40000
        elif temp < 1000:
            temp = 1000
        temp /= 100
        # print(temp)
        r,g,b = 0, 0, 0
        # cervena barva
        if temp <= 66:
            r = 255
        else:
            r = temp - 60
            r = 329.698727446 * pow(r, -0.1332047592)
            if r < 0:
                r = 0
            if r > 255:
                r = 255
        if temp <= 66:
            g = temp
            g = 99.4708025861 * nlog(g) - 161.1195681661
            if g < 0:
                g = 0
            if g > 255:
                g = 255
        else:
            g = temp - 60
            g = 288.1221695283 * pow(g, -0.0755148492)
            if g < 0:
                g = 0
            if g > 255:
                g = 255
        if temp >= 66:
            b = 255
        else:
            if temp <= 19:
                b = 0
            else:
                b = temp - 10
                b = 138.5177312231 * nlog(b) - 305.0447927307
                if b < 0:
                    b = 0
                if b > 255:
                    b = 255
        r, g, b = int(r), int(g), int(b)
        return r, g, b

    def read_general_info(self):
        orbA = self.mask_input(*self.masks["orba"])
        orbB = self.mask_input(*self.masks["orbb"])
        step = self.mask_input(*self.masks["step"])
        return clip(orbA, 500, 800), clip(orbB, 90, 150), clip(step, 110, 140)

    # =============objekty=========================
    def read_objects_count(self):
        info = self.masks["objs"]
        count = self.mask_input(*info) % self.maxCountObj
        if count == 0:
            count = self.mask_input(*info) >> 1
        return count

    def get_obj_name(self):
        tmp = self.original_string.split(' ')
        if len(tmp) > 1:
            return tmp[1][:4]
        else:
            return tmp[0][4:8].title()

    def get_object(self, idx):
        return self.mask_input(*self.masks[f"obj{idx}"])

    # precte prislusnou cast a dle ni udela planetu/pas a vrati jako tuple
    def read_object_info(self, idx):
        obj = self.get_object(idx)
        size, biom, moons, asteroid = 0, 0, 0, 0
        name = f"{self.get_obj_name()}-{idx + 1}"
        biom = self.read_object_biom(idx)
        # jedna se o pas asteroidu, ten je po celem prstenci a tak nema smysl dal cokoliv resit, pojmenovat pasy?
        if biom[0] == self.bioms[0]:
            # typ biomu - asteroidy, typ asteroidu, barva
            return {"size":None, "biom":biom[1:], "asteroids":None, "moons":None, "name":None}
        size = obj & int(0x3f)
        size = clip(size, 10, 45)
        # barva dle typu pasu
        asteroid = self.read_rings(idx)
        # provizorne barva bude z definovanych pro planety
        moons = self.read_moon(idx)
        # vracim velikost planety, jeji barvu (biom), zda ma pas asteroidu a jake barvy, jakou barvu maji mesice / proste planety
        return {"size": size, "biom": biom, "asteroids": asteroid, "moons": moons, "name": name}

    def read_moon(self, idx):
        obj = self.get_object(idx)
        moons = (obj & int(0xf0)) >> 4
        if moons >= 6 and (moons % len(self.bioms)):
            moons = (self.bioms[moons % len(self.bioms)], self.biom_environment[moons % len(self.bioms)])
        else:
            moons = None
        return moons

    def read_rings(self, idx):
        obj = self.get_object(idx)
        asteroid = obj & int(0x0f)
        # bude mit dany objekt prstenec
        if asteroid >= 8:
            asteroid = (self.asteroids[asteroid % len(self.asteroids)], self.astType[asteroid % len(self.asteroids)])
        else:
            asteroid = None
        return asteroid

    def read_object_biom(self, idx):
        obj = self.get_object(idx)
        biom = ((obj & int(0x3c)) >> 2) % len(self.bioms)
        if biom == 0:
            biom = (self.bioms[biom], self.asteroids[biom % len(self.asteroids)], self.astType[biom % len(self.astType)])
        else:
            biom = (self.bioms[biom], self.biom_environment[biom])
        return biom

    # ================Slunce=======================
    def get_sun(self, idx):
        return self.mask_input(*self.masks[f"s{idx}c"])

    def read_suns_count(self):
        info = self.masks["suns"]
        count = self.mask_input(*info) % 3
        if count == 0:
            count = 1
        return count

    # precte prislusnou cast a dle ni udela barvu a velikost, kterou vrati jako tuple
    def read_sun_info(self, idx):
        sun = self.get_sun(idx)
        #TODO osetrit jmeno slunce
        size, name = (sun & int(0x7dff) >> 4) % 270, f"{self.original_string[:4]}-{idx + 1}"
        color = self.read_sun_colors(idx)
        surface = ObjectEnvironment(sun, "", self.read_sun_colors(idx))
        surface.set_noise_exponents(nparray((0, 0, 0.03125, 0.015625)))
        return {"size": size, "surface": surface, "name": name}

    def read_sun_colors(self, idx):
        # if idx < 0 or idx >= 3:
        color = self.get_sun(idx) >> 4
        base_color = nparray(self.kelvin_to_rgb(color))
        color_range = [base_color * 2.983, base_color * 0.95, base_color * 1.15,
                       base_color * 1.87, base_color * 0.75, base_color]
        return color_range

    # ==============pozadi=========================
    def read_distant_stars(self, image_size):
        mask = self.masks["distant_stars"]
        info = self.mask_input(*mask)
        # prectu pocet
        count = info & int(0x002ff)
        # prectu count ruznych barev
        for i in range(count):
            kelvin = (info ** (i + 1)) % 30000
            # 3500 kelvina je teplota hvezdy s nejnižší povrchovou teplotou horke kavy
            while kelvin < 2000:
                kelvin = (kelvin ** (i + 1)) % 30000
                if kelvin <= 10:
                    kelvin += 20
            # ulozim do uloziste
            color = self.kelvin_to_rgb(kelvin)
            size = random.randint(low=8, high=32)
            position = (random.randint(low=0, high=image_size[0]), random.randint(low=0, high=image_size[1]))
            # print(f"({position}), {size}, ({color})")
            self.info_store.add_distant_star(DistantStar(position, size, color))

    # ===========biomy - barvy=======================
    def return_object_colors(self, idx):
        shifts = self.color_masks[f"obj{idx}"]
        resulting_colors = []
        for i in shifts:
            color = self.mask_input(0xffffff, i)
            R, G, B = color & 0xff, (color >> 4) & 0xff, (color >> 8) & 0xff
            resulting_colors.append(nparray((R, G, B)))
        resulting_colors.extend([nparray((72, 74, 71)), nparray((250, 250, 250))])
        return resulting_colors


if __name__ == "__main__":
    storage = GeneralStorage()
    par = ConstalationParser(storage)
    par.init("Jan Tislický")
    dict_of_old = { "orba":     (int(0x0000000000fff0000000000000000000000000000000000000), 37),
                    "orbb":     (int(0x0000000000000fff0000000000000000000000000000000000), 34),
                    "step":     (int(0x0000000000000000fff0000000000000000000000000000000), 31), }
    print("-"*40)
    for item in ["orba"]:#, "orbb", "step"]:
        mask, shift = par.masks[item]
        mask_old, shift_old = dict_of_old[item]
        print(hex((par.hexadecimal_representation)))
        print("0"*10 + hex(mask_old))
        print(hex((par.hexadecimal_representation & mask_old)))
        print(hex((par.hexadecimal_representation & mask_old) >> (shift_old * 4)))
        # print((par.hexadecimal_representation & mask_old) >> (shift_old * 4))
        print("+"*40)
        print(hex(par.hexadecimal_representation))
        print(hex(par.hexadecimal_representation >> (shift * 4)))
        print(hex((par.hexadecimal_representation >> (shift * 4)) & 0xfff))
        print((par.hexadecimal_representation >> (shift * 4)) & mask)
        # print(par.mask_input(mask, shift))
        print("-"*40)
