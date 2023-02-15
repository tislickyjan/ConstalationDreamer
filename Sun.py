from SpaceObject import SpaceObject


class Sun(SpaceObject):
    def __init__(self, position, size, color, name):
        super().__init__(position, size, color, name)