from SpaceObject import SpaceObject


class Asteroids(SpaceObject):
    def __init__(self, color, position, size, name):
        super().__init__(position, size, color, name)