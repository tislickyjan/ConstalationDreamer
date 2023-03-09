from numpy import array as nparr

class GeneralStorage:
    distant_stars = []
    planets = []
    suns = []
    orbA = 0
    orbB = 0
    step = 0
    number_of_planets = 10
    number_of_suns = 1
    random_position = None
    magma_palette = [nparr((255, 37, 0)), nparr((255, 102, 0)), nparr((242, 242, 23)),
                     nparr((234, 92, 15)), nparr((229, 101, 32)), nparr((38, 38, 38))]
    barren_palette = [nparr((88, 88, 88)), nparr((96, 96, 96)), nparr((111, 111, 111)),
                      nparr((128, 128, 128)), nparr((153, 153, 153)),nparr((204, 204, 204))]
    desert_palette = [nparr((5, 142, 217)), nparr((220, 164, 68)), nparr((231, 169, 103)),
                      nparr((120, 48, 9)), nparr((90, 17, 7)),nparr((47, 33, 38))]

    def set_general_information(self, info):
        self.orbA, self.orbB, self.step = info
        print(f"general info: {info}")

    def set_number_of_objects(self, no_suns, no_objects):
        self.number_of_suns, self.number_of_planets = no_suns, no_objects
        print(f"suns: {self.number_of_suns} | objects: {self.number_of_planets}")

    def set_rand_pos(self, position):
        self.random_position = position

    def return_size(self, i):
        return (self.orbA + i * self.step,
                self.orbB + i * self.step // 3)

    def add_distant_star(self, star):
        self.distant_stars.append(star)

    def clear_all_info(self):
        self.distant_stars = []
        self.planets = []
        self.suns = []
        self.orbA = 0
        self.orbB = 0
        self.step = 0
        self.number_of_planets = 10
        self.number_of_suns = 1
        self.random_position = None
