class GeneralStorage:
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

    def set_number_of_objects(self, no_suns, no_objects):
        self.number_of_suns, self.number_of_planets = no_suns, no_objects

    def set_rand_pos(self, position):
        self.random_position = position

    def return_size(self, i):
        return (self.orbA + i * self.step,
                self.orbB + i * self.step // 3)
