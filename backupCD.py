from PIL import Image, ImageDraw
import numpy as np

sun = 180
orbA,orbB = 400,75
step = 100

# vypocítava celou vyslednou soustavu na zaklade parametru, pripadne upravuje vysledek
class ConstalationDreamer:
    finalImage = None
    planets = []

    def __init__(self):
        self.imageSize = np.array((1920,1080))
        self.finalImage = Image.new("RGB",tuple(self.imageSize))
        self.drawPlace = ImageDraw.Draw(self.finalImage, 'RGBA')
        # self.numberOfPlanets = np.random.randint(low=1,high=10)
        self.numberOfPlanets = 5

    def Dream(self):
        randPos = np.random.randint(low=-15,high=15,size=self.numberOfPlanets)
        #self.GenerateSpaceEnvironment(randPos)

        self.SunOrbitalPlanets(randPos, np.pi, np.pi*2, 1, (0, self.numberOfPlanets, 1))

        self.Sun(self.imageSize/2, sun)

        self.SunOrbitalPlanets(randPos, 0, np.pi, 0, (0,self.numberOfPlanets,1))

    def GenerateSpaceEnvironment(self, randTrans):
        for i in range(self.numberOfPlanets):
            position = self.imageSize / 2 + randTrans[i]
            size = (orbA + i * step, orbB + i * step // 3)
            spaceObject = np.random.randint(low=0, high=10)
            if spaceObject >= 8:
                self.AsteroidField(position, size)
            else:
                self.PlacePlanet(size, position)

    # zatim dela jedno slunce, chci vice slunci
    def Sun(self, pos, size):
        # a = lu, b = rb
        a, b = pos - (size, size), pos + (size, size)
        self.drawPlace.ellipse((a[0], a[1], b[0], b[1]), outline=(255, 0, 0), fill=(255, 255, 0), width=3)

    def SunOrbitalPlanets(self, randTrans, minA, maxA, front, iter):
        for i in range(iter[0], iter[1], iter[2]):
            position = self.imageSize/2 + randTrans[i]
            self.DrawSunOrbital(position, (orbA+i*step,orbB+i*step//3), front, 0 if len(self.planets) < self.numberOfPlanets else self.planets[i][-1])
            if self.planets[i][-1] == -1:
                self.DrawAsteroidField(self.planets[i], front)
            elif minA <= self.planets[i][-1] <= maxA:
                self.DrawPlanet(self.planets[i])

    def DrawSunOrbital(self, pos, size, front, aster):
        spaceObject = np.random.randint(low=0,high=10)
        a, b = pos - size, pos + size
        orbColor = (100, 100, 100)
        if front:
            if spaceObject >= 8:
                self.AsteroidField(pos,size)
            else:
                self.PlacePlanet(size, pos)
                self.drawPlace.arc((a[0], a[1], b[0], b[1]),start=180,end=360,fill=orbColor, width=4)
        elif not front and aster != -1:
            self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=0, end=180, fill=orbColor, width=4)

    def PlacePlanet(self, orbSize, center):
        t = np.random.uniform(low=0.0,high=2*np.pi)
        planetPosition = np.array((orbSize[0]*np.cos(t),orbSize[1]*np.sin(t))) + center
        planetSize = np.array((20,20))
        lu, rb = planetPosition - planetSize, planetPosition + planetSize
        # print("adding Planet on position {}, with angle {}".format(planetPosition, np.rad2deg(t)))
        # bbox, velikost planety, poloha na elipse
        self.planets.append(((lu[0], lu[1], rb[0], rb[1]), planetPosition, planetSize, t))

    def DrawPlanet(self, planet):
        color = (np.random.randint(low=0, high=255), np.random.randint(low=0, high=255), np.random.randint(low=0, high=255))
        numRings = np.random.randint(low=0, high=10)
        t = np.random.uniform(low=0.0, high=2*np.pi)
        moons = np.random.randint(low=0, high=10)
        moonSize,ringSize = 5, 10
        if numRings > 4:
            print("Adding antonov ring to planet {}".format(self.planets.index(planet)))
            scaleFactor = (2,0.67)
            a, b = planet[1] - planet[2]*scaleFactor, planet[1] + planet[2]*scaleFactor
            self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=180, end=360, fill=(255,0,0), width=ringSize)
            self.drawPlace.ellipse(planet[0], fill=color)
            self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=0, end=180, fill=(255,0,0), width=ringSize)
        else:
            self.drawPlace.ellipse(planet[0], fill=color)
        if moons > 5:
            moonFac = np.array((1.75,1.75))*planet[2]
            moonPosition = np.array((np.cos(t),np.sin(t)))*moonFac + planet[1]
            lu,rb = moonPosition - moonSize, moonPosition + moonSize
            self.drawPlace.ellipse((lu[0], lu[1], rb[0], rb[1]), fill=(0,255,0))

    def AsteroidField(self, pos, size):
        asteroidColor = np.random.randint(low=0,high=3)
        colors = [(75,75,75),(30,144,255),(205,133,63)]
        self.planets.append((colors[asteroidColor],size, pos,-1))

    def DrawAsteroidField(self, field, front):
        print(f"Asteroids on position {self.planets.index(field)}")
        asteroidSize = np.array((5,5))
        amount = 100
        if front:
            asteroidPositions = np.random.uniform(low=np.pi,high=np.pi*2,size=amount)
        else:
            asteroidPositions = np.random.uniform(low=0.0,high=np.pi,size=amount)
        for t in asteroidPositions:
            astPosition = np.array((field[1][0] * np.cos(t), field[1][1] * np.sin(t))) + field[2]
            lu, rb = astPosition - asteroidSize, astPosition + asteroidSize
            self.drawPlace.ellipse((lu[0], lu[1], rb[0], rb[1]), fill=field[0])

    #TODO: Nebula effect in system
    # def AddNebula(self):
    #     ...

    #TODO: Background stars
    # def BackgroundStars(self):
    #     ...

    #TODO: Megastructures
    # def Megastructures(self):
    #    ...

    #TODO: Fauna and flora
    # def Biomes(self):
    #    ...

    #TODO: nice to have - vsechny planety budou videt a zadna nebude za sluncem

if __name__ == "__main__":
    cdreamer = ConstalationDreamer()
    cdreamer.Dream()
    cdreamer.finalImage = cdreamer.finalImage.resize((960,540), resample=Image.ANTIALIAS)
    cdreamer.finalImage.show()

    """
    rotovani planet
        tmpRotPl = Image.new("RGBA", (80,40))
        imgSize = np.array(tmpRotPl.size)
        draw = ImageDraw.Draw(tmpRotPl)
        a, b = planet[1] - planet[2]*scaleFactor, planet[1] + planet[2]*scaleFactor
        draw.arc((0, 10, 80, 30), start=180, end=360, fill=(255,0,0), width=ringSize)
        draw.ellipse((20,0,60,40), fill=color)
        draw.arc((0, 10, 80, 30), start=0, end=180, fill=(255,0,0), width=ringSize)
        rotated = tmpRotPl.rotate(0,expand=True)
        self.finalImage.paste(rotated,planet[0],rotated)
        """