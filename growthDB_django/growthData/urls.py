from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url

from . import views
from .views import WellUpdate, PlateUpdate, PlateDelete, WellList, PlateList, ExperimentalDesignList,ExperimentalDesignUpdate


app_name = 'growthData'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^well/(?P<well_id>[0-9]+)/$', views.well, name='well'),
    url(r'^well/(?P<pk>[0-9]+)/$', WellUpdate.as_view(success_url='/growthData/wells/'), name='well'),
    url(r'^wells/$', WellList.as_view(),name="wells"),
    url(r'^plates/create/$', views.create_plate, name='plateCreate'),
    url(r'^plates/$', PlateList.as_view(),name="plates"),
    url(r'^plates/(?P<plate_id>[0-9]+)/$', views.plate, name='plate'),
    url(r'^experimentalDesigns/(?P<pk>[0-9]+)/$', ExperimentalDesignUpdate.as_view(success_url='/growthData/experimentalDesigns'), name='experimentalDesign'),
    url(r'^experimentalDesigns', ExperimentalDesignList.as_view(), name='experimentalDesigns'),
]