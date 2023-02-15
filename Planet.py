from SpaceObject import SpaceObject


class Planet(SpaceObject):
    def __init__(self, name, color, bbox, position, shift, size, t, rings=False, moons=False):
        self.box = bbox
        self.t = t
        self.rings = rings
        self.moons = moons
        self.shift = shift
        super().__init__(position, size, color, name)
