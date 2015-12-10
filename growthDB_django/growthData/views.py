from django.shortcuts import render,get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView

from .models import Plate, Well, ExperimentalDesign
from .forms import PlateForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def well(request, well_id):
    return HttpResponse("You're looking at question %s." % well_id)

def plate(request, plate_id):
    # response = "You're looking at the results of plate %s."
    # return HttpResponse(response % plate_id)
    plate = get_object_or_404(Plate, pk=plate_id)
    # try:
    #     plate = Plate.objects.get(pk=plate_id)
    # except Plate.DoesNotExist:
    #     raise Http404("Plate does not exist")
    return render(request, 'growthData/plate.html', {'plate': plate})

# def plateCreate(request,):

#     return render(request, 'growthData/plateCreate.html', {})
    # question = get_object_or_404(Question, pk=question_id)
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def plateOverview(request):
    latest_plate_list = Plate.objects.order_by('-date')[:5]
    context = {'latest_plate_list': latest_plate_list}
    return render(request, 'growthData/plateOverview.html', context)

def experimentalDesign(request, ed_id):
    return HttpResponse("You're voting on experimental design %s." % ed_id)


# Plate views

# class PlateCreate(CreateView):
#     model = Plate
#     fields = ['name','project','experimenter','dataFile']

from django.utils import timezone
import pandas as pd

def handle_file(f):
	data = pd.read_csv(f)
	print data.shape

def create_plate(request):
    if request.method == 'POST':
        form = PlateForm(request.POST, request.FILES)

        if form.is_valid():
            plate = Plate(**form.cleaned_data)
            plate.save()

            wells = [Well(plate=plate,number=i,biologicalReplicate=i,experimentalDesign=None) for i in range(200)]
            [w.save() for w in wells]

            return HttpResponseRedirect('/growthData/plate/')
    else:
    	print "not post"
        form = PlateForm()
    return render(request, 'growthData/plate_form.html', {'form': form})

class PlateUpdate(UpdateView):
    model = Plate
    fields = ['name']

class PlateDelete(DeleteView):
    model = Plate
    success_url = reverse_lazy('plateOverview')

class PlateList(ListView):
    model = Plate

# Well views

class WellList(ListView):
    model = Well

class WellUpdate(UpdateView):
    model = Well
    fields = ['name']

class WellCreate(CreateView):
    model = Well
    fields = ['name']

class PlateDelete(DeleteView):
    model = Well
    success_url = reverse_lazy('well')

# Experimental Design
class ExperimentalDesignList(ListView):
    model = ExperimentalDesign