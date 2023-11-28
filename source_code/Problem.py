import math
PI = 3.141592
RRR = 6378.388
class Problem:
    def __init__(self):
        self.coordinates = []
        self.cLength = 0
        self.optimalSolution = 0
        self.problemType = ""

    def distance(self,order):
        sum = 0
        for i in range(self.cLength):
            c1 = self.coordinates[order[i%self.cLength]-1]
            c2 = self.coordinates[order[(i+1)%self.cLength]-1]
            if self.problemType == "EUC_2D":
                sum += self.euc2Dist(c1,c2)
            elif self.problemType == "GEO":
                sum += self.geoDist(c1,c2)
        return sum

    def euc2Dist(self,coord1,coord2):
        xd = coord1[1] - coord2[1]
        yd = coord1[2] - coord2[2]
        dij = int(math.sqrt(xd*xd + yd*yd) + 0.5)
        return dij

    def geoDist(self,coord1,coord2):
        q1 = math.cos(self.convRad(coord1[2]) - self.convRad(coord2[2]))
        q2 = math.cos(self.convRad(coord1[1]) - self.convRad(coord2[1]))
        q3 = math.cos(self.convRad(coord1[1]) + self.convRad(coord2[1]))
        dij = int(RRR * math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0)
        return dij

    def convRad(self,val):
        deg = int(val)
        min = val - deg
        rad = PI * (deg + 5.0 * min/3.0)/180.0
        return rad