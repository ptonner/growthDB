from django.shortcuts import render,get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Plate, Well, ExperimentalDesign, Design, DesignElement
from .forms import PlateForm, PlateDesignForm,WellReplicateForm, WellsReplicateForm
from .plate import plate_canvas, save_plate_image, handle_data

@login_required
def index(request):

    if request.user.is_authenticated():
        plates = Plate.objects.all()
        experimentalDesigns = ExperimentalDesign.objects.all()

        context = {'plates': plates, 'experimentalDesigns':experimentalDesigns}
        return render(request, 'microbial_growth_data/index.html', context)
    else:
        return HttpResponse("you're not logged in, get lost.")

# Plate views
from django.utils import timezone


@login_required
def create_plate(request):
    if request.method == 'POST':
        form = PlateForm(request.POST, request.FILES)

        if form.is_valid():

            plate = Plate(**form.cleaned_data)
            plate.save()

            data = handle_data(plate)

            # wells = [Well(plate=plate,number=i,biologicalReplicate=0,experimentalDesign=None) for i in range(numWells)]
            wells = [Well(plate=plate,number=i,biologicalReplicate=0,experimentalDesign=None) for i in data.columns[1:]]
            [w.save() for w in wells]

            return HttpResponseRedirect('plates/')
    else:
        form = PlateForm()
    return render(request, 'microbial_growth_data/plate_form.html', {'form': form})

@login_required
def design_plate(request,pk,form=None):
    plate = Plate.objects.get(id=pk)

    if request.method == 'POST':
        form = PlateDesignForm(request.POST, request.FILES)

        if form.is_valid():
            
            # ed = form.cleaned_data['experimentalDesign']
            # designElements = form.cleaned_data['designElements']
            strain = form.cleaned_data['strain']
            wellString = form.cleaned_data['wells']

            wells = []
            for w in wellString.split(","):
                # w = str(w)
                if "-" in w:
                    split = w.split("-")
                    low = int(split[0])
                    high = int(split[1])
                    w = list(Well.objects.filter(plate=plate,number__in=range(low,high+1)))
                    wells = wells + w                    
                else:
                    w = Well.objects.get(plate=plate,number=int(w))
                    wells.append(w)

            designElements = []

            for i in range(10):
                design = form.cleaned_data['design_%d'%i]
                value = form.cleaned_data['value_%d'%i]

                design, created = Design.objects.get_or_create(name=design)
                designElement,created = DesignElement.objects.get_or_create(design=design,value=value)
                designElements.append(designElement)
            # designElements = [designElement]

            designElementSet = set(designElements)
            eds = ExperimentalDesign.objects.filter(strain=strain)
            found = False
            for ed in eds:
                otherSet = set(ed.designElements.all())
                if otherSet == designElementSet:
                    found=True
                    break

            if not found:
                ed = ExperimentalDesign(strain=strain)
                ed.save()
                ed.designElements.add(*designElements)
                ed.save()

            for w in wells:
                w.experimentalDesign = ed
                w.save()
            
            # return HttpResponseRedirect('/plates/%s/design'%pk)
            from django.shortcuts import redirect
            redirect('/plates/%s/design'%pk)

    else:
        if not form:
            form = PlateDesignForm()
            form.fields['wells'].queryset = plate.well_set.all()

        # print plate.well_set.count()
    return render(request, 'microbial_growth_data/platedesign_form.html', {'form': form,'plate':plate})


@login_required
def plate_image(request,pk):

    plate = Plate.objects.get(id=pk)

    # save_plate_image(plate)

    canvas = plate_canvas(plate)

    response=HttpResponse(content_type='image/png')
    canvas.print_png(response,bbox_inches="tight",pad=0)
    return response

    # return HttpResponse(image_data, content_type="image/png")

def buildPlateContext(context,plate):

    context['well_list'] = plate.well_set.all()
    context['ed_list'] = ExperimentalDesign.objects.filter(well__in=plate.well_set.all()).distinct()
    
    expDesignWells = []
    for ed in context['ed_list']:
        wells = plate.well_set.filter(experimentalDesign=ed)
        expDesignWells.append([w.number for w in wells])

    wellStrings = []
    for wells in expDesignWells:
        s = ""
        i = 0

        while i < len(wells):
            curr = i

            while i<len(wells)-1 and wells[i]+1 == wells[i+1]:
                i+= 1

            if curr != i:
                s += "%d - %d, " % (wells[curr],wells[i])
            else:
                s += "%d, " % wells[curr]
            i+=1
        wellStrings.append(s[:-2])


    context['wellStrings'] = wellStrings

    context['expDesign_wellStrings'] = zip(context['ed_list'],wellStrings)

    return context
        

from django.forms.formsets import formset_factory

@login_required
def plate_replicate(request,pk,form=None):
    plate = Plate.objects.get(id=pk)

    if request.method == 'POST':
        # form = PlateDesignForm(request.POST, request.FILES)
        wellForms = []
        for ed in plate.experimentalDesigns():
            wells = ed.well_set.filter(plate=plate).all()
            form = WellsReplicateForm(request.POST,wells=wells)
            form.experimentalDesign=ed
            wellForms.append(form)

        # if form.is_valid():
        if all([wf.is_valid() for wf in wellForms]):

            for wf in wellForms:
                numbers = [int(f) for f in wf.fields]
                wells = Well.objects.filter(plate=plate,number__in=numbers)
                for w in wells:
                    w.biologicalReplicate = wf[f].value()
            
            # return HttpResponseRedirect('/plates/%s/design'%pk)
            from django.shortcuts import redirect
            redirect('/plates/%s/replicate'%pk)

    else:
        if not form:

            # WellReplicateFormSet = formset_factory(WellsReplicateForm)

            wellForms = []
            for ed in plate.experimentalDesigns():
                wells = ed.well_set.filter(plate=plate).all()
                form = WellsReplicateForm(wells=wells)
                form.experimentalDesign=ed
                wellForms.append(form)

            # wells = plate.well_set.all()
            # form = WellReplicateForm({'biologicalReplicate':wells[0].biologicalReplicate})
            # form.fields['biologicalReplicate'].label=wells[0].number
            

        # print plate.well_set.count()
    return render(request, 'microbial_growth_data/platereplicate_form.html', {'wellForms':wellForms,'experimentalDesigns':plate.experimentalDesigns,'plate':plate})

class PlateDetail(LoginRequiredMixin,DetailView):
    model = Plate

    def get_context_data(self, **kwargs):
        context = super(PlateDetail, self).get_context_data(**kwargs)
        context['well_list'] = self.get_object().well_set.all()#filter(plate=self.get_object())
        context['ed_list'] = ExperimentalDesign.objects.filter(well__in=self.get_object().well_set.all()).distinct()
        
        expDesignWells = []
        for ed in context['ed_list']:
            wells = self.get_object().well_set.filter(experimentalDesign=ed)
            expDesignWells.append([w.number for w in wells])

        wellStrings = []
        for wells in expDesignWells:
            s = ""
            i = 0

            while i < len(wells):
                curr = i

                while i<len(wells)-1 and wells[i]+1 == wells[i+1]:
                    i+= 1

                if curr != i:
                    s += "%d - %d, " % (wells[curr],wells[i])
                else:
                    s += "%d, " % wells[curr]
                i+=1
            wellStrings.append(s[:-2])


        context['wellStrings'] = wellStrings

        context['expDesign_wellStrings'] = zip(context['ed_list'],wellStrings)

        return context


# class PlateUpdate(UpdateView):
#     model = Plate
#     fields = ['name']

class PlateDelete(LoginRequiredMixin,DeleteView):
    model = Plate
    success_url = reverse_lazy('growthData:plates')

class PlateList(LoginRequiredMixin,ListView):
    model = Plate
    paginate_by = 10

# Well views

class WellList(LoginRequiredMixin,ListView):
    model = Well
    paginate_by = 10

class WellUpdate(LoginRequiredMixin,UpdateView):
    model = Well
    template_name_suffix = '_update_form'

    fields = ['experimentalDesign','biologicalReplicate']

# class WellCreate(CreateView):
#     model = Well
#     fields = ['name']

# class WellDelete(DeleteView):
#     model = Well
#     success_url = reverse_lazy('well')

# Experimental Design
class ExperimentalDesignList(LoginRequiredMixin,ListView):
    model = ExperimentalDesign
    paginate_by = 10

# class ExperimentalDesignUpdate(UpdateView):
class ExperimentalDesignUpdate(LoginRequiredMixin,DetailView):
    model = ExperimentalDesign

    # fields = ['strain','designElements']
    # template_name_suffix = '_update_form'
    # template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(ExperimentalDesignUpdate, self).get_context_data(**kwargs)
        context['well_list'] = self.get_object().well_set.filter(experimentalDesign=self.get_object())
        return context
