from SpaceObject import SpaceObject


class Moon(SpaceObject):
    def __init__(self, name, color, bbox, position, size, t):
        super().__init__(position,size,color,name)
        self.box = bbox
        self.t = t

    def draw(self, factor, canvas):
        ...