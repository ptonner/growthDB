from django.shortcuts import render,get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView

from .models import Plate, Well, ExperimentalDesign
from .forms import PlateForm, PlateDesignForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def well(request, well_id):
    return HttpResponse("You're looking at question %s." % well_id)

def plate(request, plate_id):
    plate = get_object_or_404(Plate, pk=plate_id)
    return render(request, 'growthData/plate.html', {'plate': plate})

def plateOverview(request):
    latest_plate_list = Plate.objects.order_by('-date')[:5]
    context = {'latest_plate_list': latest_plate_list}
    return render(request, 'growthData/plateOverview.html', context)

def experimentalDesign(request, ed_id):
    return HttpResponse("You're voting on experimental design %s." % ed_id)


# Plate views
from django.utils import timezone
import pandas as pd

def handle_file(f):
    print "handle_file"
    data = pd.read_csv(f)

    assert data.columns[0].lower() == "time"

    data = data.drop("Blank",1)

    numWells = data.shape[1] - 1

    return numWells

def create_plate(request):
    if request.method == 'POST':
        form = PlateForm(request.POST, request.FILES)

        if form.is_valid():
            numWells = handle_file(request.FILES['dataFile'])

            plate = Plate(**form.cleaned_data)
            plate.save()

            wells = [Well(plate=plate,number=i,biologicalReplicate=0,experimentalDesign=None) for i in range(numWells)]
            [w.save() for w in wells]

            return HttpResponseRedirect('/growthData/plates/')
    else:
        form = PlateForm()
    return render(request, 'growthData/plate_form.html', {'form': form})

def design_plate(request,pk):
    if request.method == 'POST':
        form = PlateDesignForm(request.POST, request.FILES)

        if form.is_valid():
            plate = Plate.objects.get(id=pk)
            # plate = Plate(**form.cleaned_data)
            ed = form.cleaned_data['experimentalDesign']
            wells = form.cleaned_data['wells']

            for w in wells:
                w.experimentalDesign = ed
                w.save()
            
            return HttpResponseRedirect('/growthData/plates/%s'%pk)
    else:
        plate = Plate.objects.get(id=pk)
        form = PlateDesignForm()
        form.fields['wells'].queryset = plate.well_set.all()

        print plate.well_set.count()
    return render(request, 'growthData/platedesign_form.html', {'form': form,'plate':plate})

class PlateDetail(DetailView):
    model = Plate

    def get_context_data(self, **kwargs):
        context = super(PlateDetail, self).get_context_data(**kwargs)
        context['well_list'] = self.get_object().well_set.filter(plate=self.get_object())
        context['ed_list'] = ExperimentalDesign.objects.filter(well__in=self.get_object().well_set.all()).distinct()
        return context


class PlateUpdate(UpdateView):
    model = Plate
    fields = ['name']

class PlateDelete(DeleteView):
    model = Plate
    success_url = reverse_lazy('growthData:plates')

class PlateList(ListView):
    model = Plate

# Well views

class WellList(ListView):
    model = Well

class WellUpdate(UpdateView):
    model = Well
    template_name_suffix = '_update_form'

    fields = ['experimentalDesign','biologicalReplicate','technicalReplicate']

class WellCreate(CreateView):
    model = Well
    fields = ['name']

class WellDelete(DeleteView):
    model = Well
    success_url = reverse_lazy('well')

# Experimental Design
class ExperimentalDesignList(ListView):
    model = ExperimentalDesign

# class ExperimentalDesignUpdate(UpdateView):
class ExperimentalDesignUpdate(DetailView):
    model = ExperimentalDesign

    # fields = ['strain','designElements']
    # template_name_suffix = '_update_form'
    # template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(ExperimentalDesignUpdate, self).get_context_data(**kwargs)
        context['well_list'] = self.get_object().well_set.filter(experimentalDesign=self.get_object())
        return context
