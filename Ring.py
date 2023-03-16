from SpaceObject import SpaceObject


class Ring(SpaceObject):
    def __init__(self, position, size, surface):
        super().__init__(position, size, surface)

    def draw(self, factor, canvas):
        ...