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
    return HttpResponse("Hello, world. You're at the growthDB index.")

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
            # numWells = handle_file(request.FILES['dataFile'])

            plate = Plate(**form.cleaned_data)
            plate.save()

            data = handle_data(plate)

            # wells = [Well(plate=plate,number=i,biologicalReplicate=0,experimentalDesign=None) for i in range(numWells)]
            wells = [Well(plate=plate,number=i,biologicalReplicate=0,experimentalDesign=None) for i in data.columns[1:]]
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
            
            return HttpResponseRedirect('/growthData/plates/%s/design'%pk)
    else:
        plate = Plate.objects.get(id=pk)
        form = PlateDesignForm()
        form.fields['wells'].queryset = plate.well_set.all()

        print plate.well_set.count()
    return render(request, 'growthData/platedesign_form.html', {'form': form,'plate':plate})

def plot_data(f):
    data = pd.read_csv(f)

    assert data.columns[0].lower() == "time"

    data = data.drop("Blank",1)

    for i in range(1,data.shape[1]):
        plt.scatter(data.iloc[:,0],data.iloc[:,i])

def parse_time(t):
    import time

    try:
        return time.struct_time(time.strptime(t,'%H:%M:%S'))
    except ValueError, e:
        try:
            t = time.strptime(t,'%d %H:%M:%S')
            t = list(t)
            t[2]+=1
            return time.struct_time(t)
        except ValueError, e:
            raise Exception("Time format unknown")

def handle_data(p):

    import datetime
    import numpy as np

    data = pd.read_csv(p.dataFile)

    assert data.columns[0].lower() == "time"
    data = data.drop("Blank",1)

    def convert_time(x):
        delta = datetime.datetime(*x[:-2]) - datetime.datetime(*t[0][:-2])
        return 24*delta.days + float(delta.seconds)/3600

    t = data.iloc[:,0].apply(parse_time)
    t = t.apply(convert_time).round(2)
    data['Time'] = t

    data.iloc[:,1:] = np.log(data.iloc[:,1:])
    data.iloc[:,1:] = data.iloc[:,1:] - data.iloc[0,1:]

    return data

def plate_canvas(p):

    data = handle_data(p)

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    import datetime
    import random

    fig=Figure()
    ax=fig.add_subplot(111)

    for i in range(1,data.shape[1]):
        ax.plot(data.iloc[:,0],data.iloc[:,i])

    ax.set_xlabel("time (h)",fontsize=20)
    ax.set_ylabel("log(od)",fontsize=20)

    canvas=FigureCanvas(fig)

    return canvas

def plate_image(request,pk):

    plate = Plate.objects.get(id=pk)
    canvas = plate_canvas(plate)

    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

    # return HttpResponse(image_data, content_type="image/png")

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
    paginate_by = 10

# Well views

class WellList(ListView):
    model = Well
    paginate_by = 10

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
