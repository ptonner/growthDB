from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Plate

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

def plateOverview(request):
    latest_plate_list = Plate.objects.order_by('-date')[:5]
    context = {'latest_plate_list': latest_plate_list}
    return render(request, 'growthData/plateOverview.html', context)

def experimentalDesign(request, ed_id):
    return HttpResponse("You're voting on experimental design %s." % ed_id)