__author__ = 'yanghan1'


from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^EditSurfaceSet/$', views.editSurfaceSet, name='editSurfaceSet'),
    url(r'^EditSurfaceSet/LensData/$', views.lensData, name='viewLensData'),
    url(r'^EditSurfaceSet/RayData/$', views.rayData, name='viewRayData'),
    url(r'^EditSurfaceSet/MeritFunction/$', views.meritFunction, name='viewRayData'),
    url(r'^EditSurfaceSet/ConfigData/$', views.configData, name='viewRayData')

]