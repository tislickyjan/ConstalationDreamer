import numpy as np
from SpaceObject import SpaceObject
from PIL import Image, ImageDraw


class DistantStar(SpaceObject):

    def __init__(self, position, size, color):
        super().__init__(position, size, color)

    def calculate_bounds(self, factor):
        return (512, 512) - np.array(self.size) * factor, (512, 512) + np.array(self.size) * factor

    def draw_ellipse(self, factor, target_draw, opacity=255):
        a, b = self.calculate_bounds(factor)
        target_draw.ellipse((a[0], a[1], b[0], b[1]), (*self.color, opacity), outline=(0, 0, 0))

    def draw(self, factor, canvas):
        # zalozit novy obrazek, je treba urcit rozumnou velikost
        auxiliary_image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        # kreslici plocha
        local_canvas = ImageDraw.Draw(auxiliary_image)
        # parametry pro paprsky
        narrowing, wider = 0.5, 5
        # prvni kriz
        self.draw_ellipse((narrowing, wider * factor), local_canvas, 180)
        self.draw_ellipse((wider * factor, narrowing), local_canvas, 180)
        # otoceni
        auxiliary_image = auxiliary_image.rotate(45, expand=False)
        # ziskani puvodni plochy
        local_canvas = ImageDraw.Draw(auxiliary_image)
        # zmena parametru
        narrowing, wider = 0.6, 4
        # druhy kriz
        self.draw_ellipse((narrowing, wider * factor), local_canvas, 225)
        self.draw_ellipse((wider * factor, narrowing), local_canvas, 225)
        # stred
        self.draw_ellipse(factor, local_canvas)
        # nohodne otoceni a zmenseni na požadovanou velikost
        auxiliary_image = auxiliary_image.rotate(np.random.randint(low=0, high=89), expand=False)
        auxiliary_image = auxiliary_image.resize((self.size, self.size), resample=Image.LANCZOS)
        # vlozit do noveho obr
        canvas.alpha_composite(auxiliary_image, tuple(self.position))


if __name__ == "__main__":
    tmpRotPl = Image.new("RGBA", (3840, 2160), (0,0,0))
    draw = ImageDraw.Draw(tmpRotPl)
    tmp_test = [((1475, 1305), 100, (255, 228, 206)),
                ((2102, 1741), 107, (202, 218, 255)),
                ((208, 2831), 120, (175, 201, 255)),
                ((1397, 1925), 117, (202, 218, 255)),
                ((139, 2506), 139, (168, 197, 255)),
                ((1273, 1236), 106, (178, 203, 255)),
                ((943, 413), 100, (198, 216, 255)),
                ((675, 1325), 106, (255, 233, 215)),
                ((963, 1029), 150, (255, 253, 249)),
                ((5, 1083), 147, (255, 196, 148)),
                ((55, 1133), 147, (255, 196, 148))
                ]
    for i in tmp_test:
        tmp = DistantStar(*i)
        tmp.draw(1, tmpRotPl)
    tmpRotPl.show()
