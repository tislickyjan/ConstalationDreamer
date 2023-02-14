from PIL import Image
import numpy as np
import Draw
import ConstalationParser as conPar
from SpaceObject import Planet, Sun, Asteroids

#sun = 180*1.48
# orbA,orbB = 400*2,75*2
# step = 120

# vypocítava celou vyslednou soustavu na zaklade parametru, pripadne upravuje vysledek
class ConstalationDreamer:
    drawTool = None
    planets = []
    suns = []
    orbA = 0
    orbB = 0
    step = 0

    def __init__(self):
        self.numberOfPlanets = 10
        self.numberOfSuns = 1
        self.drawTool = Draw.ConstalationDrawer()
        self.par = conPar.ConstalationParser()
        self.par.Init("Jan Tislický")

    def Dream(self):
        # nacti potrebne informace
        self.orbA, self.orbB, self.step = self.par.ReadGeneralInfo()
        self.numberOfSuns, self.numberOfPlanets = self.par.ReadSunsCount(), self.par.ReadObjectsCount()
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
            local_sun = self.par.ReadSunInfo(i)
            self.suns.append(Sun(position, local_sun["size"], local_sun["color"], local_sun["name"]))
        for i in range(self.numberOfPlanets):
            position = self.drawTool.imageSize / 2 + randTrans[i]
            size = (self.orbA + i * self.step, self.orbB + i * self.step // 3)
            spaceObject = self.par.ReadObjectInfo(i)
            if spaceObject["size"] is None:
                self.AsteroidField(position, size, spaceObject)
            else:
                self.PlacePlanet(position, size, spaceObject)

    def SunOrbitalPlanets(self, randTrans, angle, iter):
        for i in range(iter[0], iter[1], iter[2]):
            if type(self.planets[i]) is not Asteroids:
                position = self.drawTool.imageSize/2 + randTrans[i]
                self.drawTool.DrawSunOrbital(position, (self.orbA+i*self.step,self.orbB+i*self.step//3), angle)
            if type(self.planets[i]) is Asteroids:
                self.drawTool.DrawAsteroidField(self.planets[i], angle)
            elif angle[0] <= self.planets[i].t <= angle[1]:
                self.drawTool.DrawPlanet(self.planets[i])

    def PlacePlanet(self, pos, size, obj):
        t = np.random.uniform(low=0.0,high=2*np.pi)
        planetPosition = np.array((size[0]*np.cos(t),size[1]*np.sin(t))) + pos
        planetSize = np.array((obj["size"],obj["size"]))
        lu, rb = planetPosition - planetSize, planetPosition + planetSize
        #self.planets.append(((lu[0], lu[1], rb[0], rb[1]), planetPosition, planetSize, t))
        self.planets.append(Planet(obj["name"], obj["biom"],(lu[0], lu[1], rb[0], rb[1]), planetPosition, planetSize, t,
                                   rings=obj["asteroids"], moons=obj["moons"]))

    def AsteroidField(self, pos, size, obj):
        self.planets.append(Asteroids(obj["biom"], size, pos, obj["name"]))

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