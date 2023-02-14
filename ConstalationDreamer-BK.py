from PIL import Image
import numpy as np
import Draw
from SpaceObject import Planet, Sun, Asteroids

#sun = 180*1.48
orbA,orbB = 400*2,75*2
step = 120

# vypocítava celou vyslednou soustavu na zaklade parametru, pripadne upravuje vysledek
class ConstalationDreamer:
    drawTool = None
    planets = []
    suns = []

    def __init__(self):
        self.numberOfPlanets = 10
        self.numberOfSuns = 1
        self.drawTool = Draw.ConstalationDrawer()

    def Dream(self):
        # random displace for palnets and orbitals, asteroids...
        randPos = np.random.randint(low=-15,high=15,size=self.numberOfPlanets)
        self.GenerateSpaceEnvironment(randPos)

        self.SunOrbitalPlanets(randPos, (np.pi, np.pi*2), (self.numberOfPlanets-1, -1, -1))

        for i in range(self.numberOfSuns):
            self.drawTool.DrawSun(self.suns[i])

        self.SunOrbitalPlanets(randPos, (0, np.pi), (0,self.numberOfPlanets,1))

    def GenerateSpaceEnvironment(self, randTrans):
        for i in range(self.numberOfSuns):
            position = self.drawTool.imageSize/2 + np.array((np.random.randint(low=-200,high=200),np.random.randint(low=-20,high=20)))
            size = 180 * np.random.uniform(low=0.1,high=1.58)
            color = (np.random.randint(low=128, high=255), np.random.randint(low=250, high=255), np.random.randint(low=0, high=32))
            self.suns.append(Sun(color,position,size,f"Kappa-{i+1}"))
        for i in range(self.numberOfPlanets):
            position = self.drawTool.imageSize / 2 + randTrans[i]
            size = (orbA + i * step, orbB + i * step // 3)
            spaceObject = np.random.randint(low=0, high=10)
            if spaceObject >= 8:
                self.AsteroidField(position, size)
            else:
                self.PlacePlanet(size, position)

    def SunOrbitalPlanets(self, randTrans, angle, iter):
        for i in range(iter[0], iter[1], iter[2]):
            if type(self.planets[i]) is not Asteroids:
                position = self.drawTool.imageSize/2 + randTrans[i]
                self.drawTool.DrawSunOrbital(position, (orbA+i*step,orbB+i*step//3), angle)
            if type(self.planets[i]) is Asteroids:
                self.drawTool.DrawAsteroidField(self.planets[i], angle)
            elif angle[0] <= self.planets[i].t <= angle[1]:
                self.drawTool.DrawPlanet(self.planets[i])

    def PlacePlanet(self, orbSize, center):
        t = np.random.uniform(low=0.0,high=2*np.pi)
        planetPosition = np.array((orbSize[0]*np.cos(t),orbSize[1]*np.sin(t))) + center
        planetSize = np.array((20,20))
        lu, rb = planetPosition - planetSize, planetPosition + planetSize
        color = (np.random.randint(low=0, high=255), np.random.randint(low=0, high=255), np.random.randint(low=0, high=255))
        numRings = np.random.randint(low=0, high=10)
        moons = np.random.randint(low=0, high=10)
        #self.planets.append(((lu[0], lu[1], rb[0], rb[1]), planetPosition, planetSize, t))
        self.planets.append(Planet("jjj", color,(lu[0], lu[1], rb[0], rb[1]), planetPosition, planetSize, t,
                                   rings=numRings > 4, moons=moons > 5))

    def AsteroidField(self, pos, size):
        asteroidColor = np.random.randint(low=0,high=3)
        colors = [(75,75,75),(30,144,255),(205,133,63)]
        self.planets.append(Asteroids(colors[asteroidColor],size, pos,"kkk"))

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

    #TODO: nice to have - vsechny planety budou videt a zadna nebude za sluncem plus rovznomerne rozlozeni

if __name__ == "__main__":
    cdreamer = ConstalationDreamer()
    cdreamer.Dream()
    cdreamer.finalImage = cdreamer.drawTool.finalImage.resize(cdreamer.drawTool.imageSize, resample=Image.ANTIALIAS)
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