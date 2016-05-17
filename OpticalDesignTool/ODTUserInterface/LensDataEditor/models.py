from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import math
import numpy as np

@python_2_unicode_compatible
class Surface(models.Model):
    surfaceIndex = models.IntegerField(default=0)
    surfaceType = models.CharField(max_length=10)
    surfaceRadius = models.FloatField(default=25.0)
    surfaceRadiusOptable = models.BooleanField(default=False)

    surfaceVertexCurvature = models.FloatField(default=0.0)
    surfaceVertexCurvatureOptable = models.BooleanField(default=False)

    surfaceMaterial = models.CharField(max_length=20, default='Air')
    surfaceMaterialOptable = models.BooleanField(default=False)

    surfaceConicConstant = models.FloatField(default=0.0)
    surfaceConicConstantOptable = models.BooleanField(default=False)

    surfaceDecenterX = models.FloatField(default=0.0)
    surfaceDecenterXOptable = models.BooleanField(default=False)

    surfaceDecenterY = models.FloatField(default=0.0)
    surfaceDecenterYOptable = models.BooleanField(default=False)

    surfaceThickness = models.FloatField(default=0.0)
    surfaceThicknessOptable = models.BooleanField(default=False)


    def __str__(self):
        return self.surfaceType

    def ZFunc(self, x, y):
        return self.surfaceVertexCurvature * self.AFunc(x, y) / (1 + self.DenomFunc(x, y))

    def AFunc(self, x, y):
        return math.pow(x - self.surfaceDecenterX, 2) + math.pow(y - self.surfaceDecenterY, 2)


    def DenomFunc(self, x, y):
        return math.sqrt(max(0, 1 - (1 + self.surfaceConicConstant) \
            * math.pow(self.surfaceVertexCurvature, 2) * self.AFunc(x, y)))

    def DzdaFunc(self, x, y):
        denom = self.DenomFunc(x, y)
        return self.surfaceVertexCurvature/(1 + denom) + 0.5 * math.pow(self.surfaceVertexCurvature, 3) *\
            self.AFunc(x, y) * (1 + self.surfaceConicConstant)/denom/math.pow(1 + denom, 2)


    def ZNormFunc(self, x, y):
        tmp = self.DzdaFunc(x, y) * 2
        n = [tmp * (x - self.surfaceDecenterX), tmp * (y - self.surfaceDecenterY), -1]
        return n / np.norm(n)

    def RefractiveIndex(self, wl):
        mat = Material.objects.get(Composition=self.surfaceMaterial)

        wl2 = math.pow(wl, 2)
        n2 = 1 + mat.A1 * wl2 / (wl2 - mat.B1) + mat.A2 * wl2 / (wl2 - mat.B2) + mat.A3 * wl2 / (wl2 - mat.B3)

        return math.sqrt(n2)


    def BendByWindow(self, point, ri):

        # lastSurface = Surface.objects.get(surfaceIndex=self.surfaceIndex - 1)
        # ri

        nvec = self.ZNormFunc(point.x, point.y)
        ivec = [math.sin(point.theta) * math.cos(point.phi),
                math.sin(point.theta) * math.cos(point.phi),
                math.cos(point.theta)]
        avec = ivec - np.dot(ivec, nvec) * nvec
        ovec = np.sign(np.dot(ivec, nvec)) * nvec + avec/math.sqrt(math.pow(ri, 2) - np.dot(avec, avec))
        ovec /= np.norm(ovec)

        theta = math.acos(ovec[2])
        phi = math.atan2(ovec[1], ovec[0])
        return [point.x, point.y, point.z, theta, phi]

    def BendByMirror(self, point):

        nvec = self.ZNormFunc(point.x, point.y)
        ivec = [math.sin(point.theta) * math.cos(point.phi),
                math.sin(point.theta) * math.cos(point.phi),
                math.cos(point.theta)]

        ovec = ivec - 2 * nvec * np.dot(ivec, nvec)
        theta = math.acos(ovec[2])
        phi = math.atan2(ovec[1], ovec[0])
        return [point.x, point.y, point.z, theta, phi]

    def BendByScatterer(self, point):
        return point

@python_2_unicode_compatible
class RaySet(models.Model):
    raySetIndex = models.IntegerField()
    raySetGridType = models.CharField(max_length=20)
    raySetGridDensity = models.IntegerField(default=4)
    raySetAngleX = models.FloatField(default=0.0)
    raySetAngleY = models.FloatField(default=0.0)
    raySetWavelength = models.FloatField(default=0.55)

    def __str__(self):
        return str(self.raySetGridType)


@python_2_unicode_compatible
class Material(models.Model):
    Composition = models.CharField(max_length=100)
    A1 = models.FloatField(default=0.0)
    B1 = models.FloatField(default=0.0)
    A2 = models.FloatField(default=0.0)
    B2 = models.FloatField(default=0.0)
    A3 = models.FloatField(default=0.0)
    B3 = models.FloatField(default=0.0)

    def __str__(self):
        return self.Composition