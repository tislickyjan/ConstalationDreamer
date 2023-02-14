class SpaceObject:
    def __init__(self, position, size, color, name=""):
        self.position = position
        self.size = size
        self.color = color
        self.name = name

class Planet(SpaceObject):
    def __init__(self, name, color, bbox, position, size, t, rings = False, moons = False):
        self.box = bbox
        self.t = t
        self.rings = rings
        self.moons = moons
        super().__init__(position,size, color, name)

class Moon(SpaceObject):
    def __init__(self, name, color, bbox, position, size, t):
        super().__init__(position,size,color,name)
        self.box = bbox
        self.t = t

class Ring(SpaceObject):
    def __init__(self, position, size, color):
        super().__init__(position, size, color)

class Asteroids(SpaceObject):
    def __init__(self, color, position, size, name):
        super().__init__(position, size, color, name)

class Sun(SpaceObject):
    def __init__(self, position, size, color, name):
        super().__init__(position, size, color, name)