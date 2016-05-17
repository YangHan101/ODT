__author__ = 'yanghan1'

import math

class Point(object):
    def __init__(self, x, y, z, theta, phi):
        if x and y and z and theta and phi :
            self.x = x
            self.y = y
            self.z = z
            self.theta = theta;
            self.phi = phi;
        else:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.theta = 0;
            self.phi = 0

    def Distance(self, point2):
        return math.sqrt((self.x - point2.x)**2 +(self.y - point2.y)**2 +(self.z - point2.z)**2)

class Ray(object):

    def __init__(self):
        self.startPoint = Point()
        self.keyPoints = []
        self.phase = []
        self._wavelengths = 0.55
        self.intensity = 1.0
        self.polarizaton = [1, 0, 0]


class Rays(object):

    def __init__(self):
        self.rayList = []

    def PropagateToNext(self, thisSurface, nextSurface):

        if self.keyPoints:
            lastCheckPt = self.keyPoints[-1]
        else:
            lastCheckPt = self.startPoint

        deltaZ = nextSurface.zFunc(lastCheckPt.x, lastCheckPt.y) - lastCheckPt.z

        tol = 1e-12
        while abs(deltaZ) > tol:

            dzdt = math.cos(lastCheckPt.theta) \
                - (nextSurface.normalDirection[0])*math.sin(lastCheckPt.theta)*math.cos(lastCheckPt.phi) \
                - (nextSurface.normalDirection[1])*math.sin(lastCheckPt.theta)*math.sin(lastCheckPt.phi)

            deltat = deltaZ / dzdt

            lastCheckPt.x += deltat * math.sin(lastCheckPt.theta) * math.cos(lastCheckPt.phi)
            lastCheckPt.y += deltat * math.sin(lastCheckPt.theta) * math.sin(lastCheckPt.phi)
            lastCheckPt.z += deltat * math.cos(lastCheckPt.theta)

            deltaZ = nextSurface.zFunc(lastCheckPt.x, lastCheckPt.y) - lastCheckPt.z

        if nextSurface.type == 'Mirror':
            lastCheckPt = self.ReflectedAtSurface(lastCheckPt, nextSurface)
        elif nextSurface.type == 'Window':
            lastCheckPt = self.RefractedatSurfaces(lastCheckPt, thisSurface, nextSurface)

        self.keyPoints.append(lastCheckPt)

        tmp_ = self.phase[-1]
        tmp_ += self.keyPoints[-1].Distance(self.keyPoints[-2]) / self._wavelengths * 2 * math.pi
        self.phase.append(tmp_)

    def ReflectedAtSurface(self, point, surface):

        nVec = surface.normalDirection(point.x, point.y)


        return point

    def RefractedBetweenSurfaces(self, point, thisSurface, nextSurface):
        return point

    def ScatteredBySurface(self, surface):
        pass

    def TraceThrough(self, surfaces):
        pass



