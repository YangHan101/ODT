__author__ = 'yanghan1'

import math
from .models import Surface, RaySet


class Point(object):
    def __init__(self, x, y, z, theta, phi):
        if x and y and z and theta and phi:
            self.x = x
            self.y = y
            self.z = z
            self.theta = theta
            self.phi = phi
        else:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
            self.theta = 0.0
            self.phi = 0.0

    def DistanceFrom(self, point2):
        return math.sqrt((self.x - point2.x)**2 + (self.y - point2.y)**2 + (self.z - point2.z)**2)


class Ray(object):

    def __init__(self, startPoint, wavelength=0.55, phase=0, intensity=1.0, polarization=0):
        # self.startPoint = Point()
        self.keyPoints = []
        self.keyPoints.append(startPoint)
        self.phase = [phase]
        self._wavelengths = wavelength
        self.intensity = intensity
        self.polarizaton = polarization

    # def PropagateToNext(self, thisSurface, nextSurface):
    #
    #     lastCheckPt = self.keyPoints[-1]
    #
    #     deltaZ = nextSurface.zFunc(lastCheckPt.x, lastCheckPt.y) - lastCheckPt.z
    #
    #     tol = 1e-12
    #     while abs(deltaZ) > tol:
    #
    #         dzdt = math.cos(lastCheckPt.theta) \
    #             - (nextSurface.normalDirection[0])*math.sin(lastCheckPt.theta)*math.cos(lastCheckPt.phi) \
    #             - (nextSurface.normalDirection[1])*math.sin(lastCheckPt.theta)*math.sin(lastCheckPt.phi)
    #
    #         deltat = deltaZ / dzdt
    #
    #         lastCheckPt.x += deltat * math.sin(lastCheckPt.theta) * math.cos(lastCheckPt.phi)
    #         lastCheckPt.y += deltat * math.sin(lastCheckPt.theta) * math.sin(lastCheckPt.phi)
    #         lastCheckPt.z += deltat * math.cos(lastCheckPt.theta)
    #
    #         deltaZ = nextSurface.zFunc(lastCheckPt.x, lastCheckPt.y) - lastCheckPt.z
    #
    #     if nextSurface.type == 'Mirror':
    #         lastCheckPt = self.ReflectedAtSurface(lastCheckPt, nextSurface)
    #     elif nextSurface.type == 'Window':
    #         lastCheckPt = self.RefractedatSurfaces(lastCheckPt, thisSurface, nextSurface)
    #
    #     self.keyPoints.append(lastCheckPt)
    #
    #     tmp_ = self.phase[-1]
    #     tmp_ += self.keyPoints[-1].Distance(self.keyPoints[-2]) / self._wavelengths * 2 * math.pi
    #     self.phase.append(tmp_)


class Rays(object):

    def __init__(self):
        self.rayList = []

    def ComputeStartPoints(self, gridType, gridDensity):
        # generate grid on unit radius circle
        grid = []
        return grid

    def InitializeRays(self):
        source = Surface.objects.get(surfaceType='source')
        if len(source) == 0 or len(source) > 1:
            pass
            # Report Error: improper source defined etc.
        else:
            # Populate the Rays

            allRaysets = RaySet.object.all()
            for rayset in allRaysets:
                # Calculate the starting Points
                unitDx = math.tan(rayset.raySetAngleX / math.pi * 180)
                unitDY = math.tan(rayset.raySetAngleY / math.pi * 180)

                theta = math.atan(math.sqrt(math.pow(unitDx, 2) + math.pow(unitDY, 2)))
                phi = math.atan(unitDY/unitDx)

                gridPoints = self.ComputeStartPoints(rayset.raySetGridType, rayset.raySetGridDensity)
                for point in gridPoints:
                    startPoint = Point(point.x * source.surfaceRadius, point.y * source.surfaceRadius, 0, theta, phi)
                    newRay = Ray(startPoint, wavelength=rayset.raySetWavelength)
                    self.rayList.append(newRay)

    def PropagateBetween(self, startIndex, endIndex):
        surfaces = Surface.objects.order_by('surfaceIndex')
        accumZ = 0
        for ii in range(startIndex):
            accumZ += surfaces[ii].surfaceThickness
        for ii in range(startIndex, endIndex + 1):
            accumZ += surfaces[ii].surfaceThickness  # The z position of the (ii+1)th surface center
            self.PropagateFrom(surfaces[ii-1], surfaces[ii], accumZ)


    def PropagateFrom(self, thisSurface, nextSurface, accumZ):

        # c = nextSurface.surfaceVertexCurvature
        # k = nextSurface.surfaceConicConstant
        # dx = nextSurface.surfaceDecenterX
        # dy = nextSurface.surfaceDecenterY
        #
        # aFunc = lambda pt: math.pow(pt[0] - dx, 2) + math.pow(pt[1] - dy, 2)
        # denomFunc = lambda pt: math.sqrt(max(0, 1-(1+k) * math.pow(c, 2) * aFunc(pt)))
        # zFunc = lambda pt: accumZ + c * aFunc(pt) / (1 + denomFunc(pt))
        # dzdaFunc =lambda pt: (c/(1 + denomFunc(pt)) + 0.5 * math.pow(c, 3) * aFunc(pt) * (1 + k)/denomFunc(pt)/math.pow(1 + denomFunc(pt), 2))
        #
        # zNormFunc = lambda pt: [dzdaFunc(pt) * 2 * (pt[0] - dx), dzdaFunc(pt) * 2 * (pt[1] - dy), -1]
        ri = lambda wl: getattr(nextSurface, 'RefractiveIndex')(wl) / getattr(thisSurface, 'RefractiveIndex')(wl)
        for ray in self.rayList:
            checkpoint = ray.keyPoints[nextSurface.surfaceIndex - 1]

            deltaz = accumZ + getattr(nextSurface, 'ZFunc')(checkpoint.x, checkpoint.y) - checkpoint.z

            tol = 1e-12
            while abs(deltaz) > tol:

                n = getattr(nextSurface, 'ZNormFunc')(checkpoint.x, checkpoint.y)

                dzdt = math.cos(checkpoint.theta) \
                    + (n[0]) * math.sin(checkpoint.theta)*math.cos(checkpoint.phi) \
                    + (n[1]) * math.sin(checkpoint.theta)*math.sin(checkpoint.phi)

                deltat = deltaz / dzdt


                checkpoint.x += deltat * math.sin(checkpoint.theta) * math.cos(checkpoint.phi)
                checkpoint.y += deltat * math.sin(checkpoint.theta) * math.sin(checkpoint.phi)
                checkpoint.z += deltat * math.cos(checkpoint.theta)

                deltaz = accumZ + getattr(nextSurface, 'ZFunc')(checkpoint.x, checkpoint.y) - checkpoint.z

            checkpoint = getattr(nextSurface, 'BendBy' + nextSurface.surfaceType)(checkpoint, ri(ray._wavelengths))

            ray.keyPoints.append(checkpoint)

            tmp_ = ray.phase[-1]
            tmp_ += ray.keyPoints[-1].Distance(ray.keyPoints[-2]) / ray._wavelengths * 2e3 * math.pi
            ray.phase.append(tmp_)



    def TraceThrough(self, surfaces):
        pass