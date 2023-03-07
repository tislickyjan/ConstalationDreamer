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
