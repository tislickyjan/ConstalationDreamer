from PIL import Image, ImageDraw
import numpy as np

class ConstalationDrawer:
    finalImage = None

    def __init__(self):
        self.imageSize = np.array((1920*2,1080*2)) # FULLHD
        # self.imageSize = np.array((7680*2,4320*2)) # 8K
        self.finalImage = Image.new("RGB",tuple(self.imageSize))
        self.drawPlace = ImageDraw.Draw(self.finalImage, 'RGBA')
        # self.multFac = 4 # 1 pro fullHD
        self.multFac = 1.6 # 8 pro 8K, funguje jako zoom

    def CalculateBounds(self, pos, size):
        return pos - np.array(size) * self.multFac, pos + np.array(size) * self.multFac

    def DrawSun(self, sun):
        a, b = self.CalculateBounds(sun.position, (sun.size, sun.size))
        outline = tuple(np.clip(sun.color + np.array((100,-50,-30)),0,255))
        self.drawPlace.ellipse((a[0], a[1], b[0], b[1]), outline=outline, fill=sun.color, width=3)

    def DrawSunOrbital(self, pos, size, angle):
        a, b = self.CalculateBounds(pos,size)
        orbColor = (60, 60, 60)
        self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=np.rad2deg(angle[0]), end=np.rad2deg(angle[1]), fill=orbColor, width=3)

    def DrawPlanet(self, planet):
        t = np.random.uniform(low=0.0, high=2*np.pi)
        moonSize, ringSize = 5, 10
        # spravna pozice dle skalovani
        planetTruePos = planet.position * self.multFac + planet.shift
        pa,pb = self.CalculateBounds(planetTruePos, planet.size)
        if planet.rings is not None:
            #print("Adding antonov ring to planet {}".format(self.planets.index(planet)))
            scaleFactor = (2,0.67)
            # a, b = planet.position - planet.size*scaleFactor, planet.position + planet.size*scaleFactor
            a, b = self.CalculateBounds(planetTruePos, planet.size*scaleFactor)
            self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=180, end=360, fill=planet.rings[0], width=ringSize)
            self.drawPlace.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=planet.color[0])
            self.drawPlace.arc((a[0], a[1], b[0], b[1]), start=0, end=180, fill=planet.rings[0], width=ringSize)
        else:
            self.drawPlace.ellipse((pa[0], pa[1], pb[0], pb[1]), fill=planet.color[0])
        if planet.moons is not None:
            moonFac = np.array((1.75,1.75))*planet.size
            moonPosition = np.array((np.cos(t),np.sin(t)))*moonFac + planetTruePos
            # lu,rb = moonPosition - moonSize, moonPosition + moonSize
            lu,rb = self.CalculateBounds(moonPosition, moonSize)
            self.drawPlace.ellipse((lu[0], lu[1], rb[0], rb[1]), fill=planet.moons[0])

    def DrawAsteroidField(self, field, angle):
        #print(f"Asteroids on position {self.planets.index(field)}")
        amount = 175
        corr, ccorr = 12, 30
        corrMod = (-1,0,1)
        for i in corrMod:
            asteroidPositions = np.random.uniform(low=angle[0],high=angle[1],size=amount)
            for t in asteroidPositions:
                tmp = np.random.randint(low=1,high=7)
                asteroidSize = np.array((tmp,tmp))
                astPosition = np.array((field.position[0] * np.cos(t), field.position[1] * np.sin(t))) * self.multFac\
                              + field.size
                dir = astPosition - self.imageSize / 2
                astPosition += i*corr*(dir/np.linalg.norm(dir))
                # lu, rb = astPosition - asteroidSize, astPosition + asteroidSize
                lu, rb = self.CalculateBounds(astPosition, asteroidSize)
                self.drawPlace.ellipse((lu[0], lu[1], rb[0], rb[1]),
                                       fill=tuple(field.color[-1]-np.array((i*ccorr, i*ccorr, i*ccorr))))