from numpy import log as nlog

class ConstalationParser:
    origString = None
    hexRepre = None
    hexLen = None
    maxCountObj = 11

    # slovnik s maskami jednotlivych casti, cislo na druhem miste udava pocet nul zprava
    masks = {
        "suns" : (int(0xf0000000000000000000000000000000000000000000000000),49),
        "s0c"  : (int(0x0ffff000000000000000000000000000000000000000000000),45),
        "s1c"  : (int(0x000ffff0000000000000000000000000000000000000000000),43),
        "s2c"  : (int(0x000000ffff0000000000000000000000000000000000000000),40),
        "orba" : (int(0x0000000000fff0000000000000000000000000000000000000),39),
        "orbb" : (int(0x0000000000000fff0000000000000000000000000000000000),34),
        "step" : (int(0x0000000000000000fff0000000000000000000000000000000),31),
        "objs" : (int(0x000000000000000000000000f0000000000000000000000000),25),
        "obj0" : (int(0x0000000000000000000000000ff00000000000000000000000),23),
        "obj1" : (int(0x000000000000000000000000000ff000000000000000000000),21),
        "obj2" : (int(0x00000000000000000000000000000ff0000000000000000000),19),
        "obj3" : (int(0x0000000000000000000000000000000ff00000000000000000),17),
        "obj4" : (int(0x000000000000000000000000000000000ff000000000000000),15),
        "obj5" : (int(0x00000000000000000000000000000000000ff0000000000000),13),
        "obj6" : (int(0x0000000000000000000000000000000000000ff00000000000),11),
        "obj7" : (int(0x000000000000000000000000000000000000000ff000000000),9),
        "obj8" : (int(0x00000000000000000000000000000000000000000ff0000000),7),
        "obj9" : (int(0x0000000000000000000000000000000000000000000ff00000),5),
        "obj10": (int(0x000000000000000000000000000000000000000000000ff000),3),
        "obj11": (int(0x00000000000000000000000000000000000000000000000ff0),1),
    }

    bioms = [
        (0,0,0), # asteroids
        (247, 70, 3), # lava
        (51, 102, 255), # ocean
        (102, 153, 0), # desert
        (128, 128, 128), # barren
        (0, 153, 51), # forrest
        (85, 128, 0), # terran
    ]

    biEn = [
        "asteroids",
        "lava",
        "ocean",
        "desert",
        "barren",
        "forrest",
        "terran",
    ]

    asteroids = [
        (75, 75, 75), (30, 144, 255), (205, 133, 63)
    ]

    astType = ["rocks", "ice", "metals&rocks"]

    def Init(self, text):
        self.origString = text
        try :
            self.hexRepre = int(self.origString.encode('utf-8'), 16)
        except (ValueError):
            self.hexRepre = int(self.origString.encode('utf-8').hex(), 16)
        self.hexLen = len(hex(self.hexRepre))-2

        while self.hexLen < 50:
            self.hexRepre += int(hex(self.hexRepre**2 * self.hexLen), 16)
            self.hexLen = len(hex(self.hexRepre))-2
        if self.hexLen > 50:
            self.hexRepre = int(str(hex(self.hexRepre))[:52],16)
            self.hexLen = len(hex(self.hexRepre))-2
        # print(int(str(hex(self.hexRepre))[:50],16))

    def MaskInput(self, mask, offset):
        shift = self.hexLen - offset
        res = (self.hexRepre & mask) >> ((self.hexLen - shift)*4)
        return res

    # source: https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
    def KelvinToRGB(self, temp):
        # print(temp)
        if temp > 40000:
            temp = 40000
        elif temp < 1000:
            temp = 1000
        temp /= 100
        # print(temp)
        r,g,b = 0,0,0
        # cervena barva
        if temp <= 66:
            r = 255
        else:
            r = temp - 60
            r = 329.698727446 * pow(r, -0.1332047592)
            if r < 0:
                r = 0
            if r > 255:
                r = 255
        if temp <= 66:
            g = temp
            g = 99.4708025861 * nlog(g) - 161.1195681661
            if g < 0:
                g = 0
            if g > 255:
                g = 255
        else:
            g = temp - 60
            g = 288.1221695283 * pow(g, -0.0755148492)
            if g < 0:
                g = 0
            if g > 255:
                g = 255
        if temp >= 66:
            b = 255
        else:
            if temp <= 19:
                b = 0
            else:
                b = temp - 10
                b = 138.5177312231 * nlog(b) - 305.0447927307
                if b < 0:
                    b = 0
                if b > 255:
                    b = 255
        r, g, b = int(r), int(g), int(b)
        return r, g, b

    def ClampVal(self, val, min, max):
        if val < min:
            return min
        if val > max:
            return max
        return val

    def ReadGeneralInfo(self):
        orbA = self.MaskInput(self.masks["orba"][0], self.masks["orba"][1])
        orbB = self.MaskInput(self.masks["orbb"][0], self.masks["orbb"][1])
        step = self.MaskInput(self.masks["step"][0], self.masks["step"][1])
        return self.ClampVal(orbA, 500, 800), self.ClampVal(orbB, 90, 150), self.ClampVal(step, 110,140)

    # =============objekty=========================
    def ReadObjectsCount(self):
        info = self.masks["objs"]
        count = self.MaskInput(info[0], info[1]) % self.maxCountObj
        if count == 0:
            count = self.MaskInput(info[0], info[1]) >> 1
        return count

    def GetObjName(self):
        tmp = self.origString.split(' ')
        if len(tmp) > 1:
            return tmp[1][:4]
        else:
            return tmp[0][4:8].title()

    # precte prislusnou cast a dle ni udela planetu/pas a vrati jako tuple
    def ReadObjectInfo(self, idx):
        info = self.masks[f"obj{idx}"]
        obj = self.MaskInput(info[0], info[1])
        size, biom, moons, asteroid = 0, 0, 0, 0
        name = f"{self.GetObjName()}-{idx+1}"
        biom = self.ReadObjectBiom(idx)
        # jedna se o pas asteroidu, ten je po celem prstenci a tak nema smysl dal cokoliv resit, pojmenovat pasy?
        if len(biom) == 3:
            # typ biomu - asteroidy, typ asteroidu, barva
            return {"size":None, "biom":biom, "asteroids":None, "moons":None, "name":None}
        size = obj & int(0x3f)
        size = self.ClampVal(size, 10, 45)
        # barva dle typu pasu
        asteroid = self.ReadRings(idx)
        # provizorne barva bude z definovanych pro planety
        moons = self.ReadMoon(idx)
        # vracim velikost planety, jeji barvu (biom), zda ma pas asteroidu a jake barvy, jakou barvu maji mesice / proste planety
        return {"size":size, "biom":biom, "asteroids":asteroid, "moons":moons, "name":name}

    def ReadMoon(self, idx):
        info = self.masks[f"obj{idx}"]
        obj = self.MaskInput(info[0], info[1])
        moons = (obj & int(0xf0)) >> 4
        if moons >= 6 and (moons % len(self.bioms)):
            moons = (self.bioms[moons % len(self.bioms)], self.biEn[moons % len(self.bioms)])
        else:
            moons = None
        return moons

    def ReadRings(self, idx):
        info = self.masks[f"obj{idx}"]
        obj = self.MaskInput(info[0], info[1])
        asteroid = obj & int(0x0f)
        # bude mit dany objekt prstenec
        if asteroid >= 8:
            asteroid = (self.asteroids[asteroid % len(self.asteroids)], self.astType[asteroid % len(self.asteroids)])
        else:
            asteroid = None
        return asteroid

    def ReadObjectBiom(self, idx):
        info = self.masks[f"obj{idx}"]
        obj = self.MaskInput(info[0], info[1])
        biom = ((obj & int(0x3c)) >> 2) % len(self.bioms)
        if biom == 0:
            biom = (self.bioms[biom], self.astType[biom % len(self.astType)], self.asteroids[biom % len(self.asteroids)])
        else:
            biom = (self.bioms[biom], self.biEn[biom])
        return biom

    # ================Slunce=======================
    def ReadSunsCount(self):
        info = self.masks["suns"]
        count = self.MaskInput(info[0], info[1]) % 3
        if count == 0:
            count = 1
        return count

    # precte prislusnou cast a dle ni udela barvu a velikost, kterou vrati jako tuple
    def ReadSunInfo(self, idx):
        info = self.masks[f"s{idx}c"]
        sun = self.MaskInput(info[0], info[1])
        #TODO osetrit jmeno slunce
        size, name = (sun & int(0x7dff) >> 4) % 270, f"{self.origString[:4]}-{idx+1}"
        color = self.ReadSunColor(idx)
        return {"size": size, "color": color, "name": name}

    def ReadSunColor(self, idx):
        # if idx < 0 or idx >= 3:
        info = self.masks[f"s{idx}c"]
        color = self.MaskInput(info[0], info[1]) >> 4
        r, g, b = self.KelvinToRGB(color)
        return r, g, b

if __name__ == "__main__":
    par = ConstalationParser()
    par.Init("Jan Tislický")
    # par = ConstalationParser("0x236f97f5a5b55cc9d")
    # mask = int(0x0fff0000000000000000000000000000000000000000000000) # numZeros = 1
    # numZeros = par.hexLen - 46
    # print(mask)
    print(par.origString)
    print(hex(par.hexRepre))
    # print(hex(par.hexRepre & mask))
    # print(f"Hex zapsany vysledek maskovani a posunuty vpravo {hex((par.hexRepre & mask)>>par.hexLen*4-(numZeros*4))}")
    # print(f"Vysledne cislo z retezu {((par.hexRepre & mask)>>par.hexLen*4-(numZeros*4))}")
    print(f"snim o {par.ReadSunsCount()} hvezde")
    print(f"kde je {par.ReadObjectsCount()} hvezdnych objektu")
    # print(par.ReadSunColor(0))
    # print(f"hvezda ma velikost {par.ReadSunInfo(1)[0]} a jemnuje se {par.ReadSunInfo(1)[1]}")
    for i in range(par.ReadObjectsCount()):
        print(par.ReadObjectInfo(i))
    # print(par.ReadObjectInfo(0))
    # print(par.ReadObjectBiom(0))
    print(par.ReadGeneralInfo())