from django.conf.urls import url

from . import views
from .views import PlateUpdate, PlateDelete, WellList, PlateList, ExperimentalDesignList


app_name = 'growthData'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^well/(?P<well_id>[0-9]+)/$', views.well, name='well'),
    url(r'^wells/$', WellList.as_view(),name="wells"),
    url(r'^plates/create/$', views.create_plate, name='plateCreate'),
    url(r'^plates/$', PlateList.as_view(),name="plates"),
    url(r'^plates/(?P<plate_id>[0-9]+)/$', views.plate, name='plate'),
    url(r'^experimentalDesigns/(?P<ed_id>[0-9]+)/$', views.experimentalDesign, name='experimentalDesign'),
    url(r'^experimentalDesigns', ExperimentalDesignList, name='experimentalDesigns'),
]