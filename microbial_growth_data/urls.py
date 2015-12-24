from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from . import views
from .views import WellUpdate, PlateUpdate, PlateDelete, WellList, PlateList,\
         ExperimentalDesignList, ExperimentalDesignUpdate, PlateDetail

from .models import Design, DesignElement, ExperimentalDesign, Plate, Strain, Project,Experimenter

app_name = 'growthData'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wells/(?P<pk>[0-9]+)/$', WellUpdate.as_view(success_url='/growthData/wells/'), name='well'),
    url(r'^wells/$', WellList.as_view(),name="wells"),

    url(r'^plates/create/$', views.create_plate, name='plate-create'),
    url(r'^plates/$', PlateList.as_view(),name="plates"),
    url(r'^plates/(?P<pk>[0-9]+)/$', PlateDetail.as_view(), name='plate'),
    url(r'^plates/(?P<pk>[0-9]+)/delete$', PlateDelete.as_view(), name='plate-delete'),
    # url(r'^plates/(?P<pk>[0-9]+)/update/$', UpdateView.as_view(model=Plate,fields=['name','experimenter','project'],success_url='/growthData/plates/'), name='plate-update'),
    url(r'^plates/(?P<pk>[0-9]+)/design/', views.design_plate, name='plate-design'),
    url(r'^plates/(?P<pk>[0-9]+)/image$', views.plate_image, name='plate-image'),

    # url(r'^experimentalDesigns/(?P<pk>[0-9]+)/$', ExperimentalDesignUpdate.as_view(success_url='/growthData/experimentalDesigns'), name='experimentalDesign'),
    url(r'^experimentalDesigns/(?P<pk>[0-9]+)/$', ExperimentalDesignUpdate.as_view(), name='experimentalDesign'),
    url(r'^experimentalDesigns/create$', CreateView.as_view(model=ExperimentalDesign,fields=['strain','designElements'],success_url='/growthData/experimentalDesigns/'), name='experimentalDesign-create'),
    url(r'^experimentalDesigns/$', ExperimentalDesignList.as_view(), name='experimentalDesigns'),
    
    url(r'^designs/$', ListView.as_view(model=Design), name='designs'),
    url(r'^designs/(?P<pk>[0-9]+)$', UpdateView.as_view(model=Design,fields=['name','description','type'],success_url='/designs/'), name='design'),
    url(r'^designs/create$', CreateView.as_view(model=Design,fields=['name','description','type'],success_url='/designs/'), name='design-create'),

    url(r'^designElements/$', ListView.as_view(model=DesignElement), name='designElements'),
    url(r'^designElements/create$', CreateView.as_view(model=DesignElement,fields=['design','value'],success_url='designElements/'), name='designElement-create'),
    # url(r'^designElements/(?P<pk>[0-9]+)$', UpdateView.as_view(model=DesignElement,fields=['design','value'],success_url='/growthData/designElements/'), name='designElement'),
    url(r'^designElements/(?P<pk>[0-9]+)$', DetailView.as_view(model=DesignElement), name='designElement'),

    url(r'^strains/$', ListView.as_view(model=Strain), name='strains'),
    url(r'^strains/create$', CreateView.as_view(model=Strain,fields=['name','parent'],success_url='/strains/'), name='strain-create'),
    url(r'^strains/(?P<pk>[0-9]+)$', DetailView.as_view(model=Strain), name='strain'),

    url(r'^projects/$', ListView.as_view(model=Project), name='projects'),
    url(r'^projects/create/$', CreateView.as_view(model=Project,fields=['name','description'],success_url='/projects/'), name='project-create'),
    url(r'^project/(?P<pk>[0-9]+)$', DetailView.as_view(model=Project), name='project'),

    url(r'^experimenters/$', ListView.as_view(model=Experimenter), name='experimenters'),
    url(r'^experimenters/create/$', CreateView.as_view(model=Experimenter,fields=['name','email'],success_url='/experimenters/'), name='experimenter-create'),
    url(r'^experimenter/(?P<pk>[0-9]+)$', DetailView.as_view(model=Experimenter), name='experimenter'),
    url(r'^experimenter/(?P<pk>[0-9]+)/delete$', DeleteView.as_view(model=Experimenter,success_url="/experimenters"), name='experimenter-delete'),
]