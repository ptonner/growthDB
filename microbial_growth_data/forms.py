from django import forms
from .models import Project, Experimenter, ExperimentalDesign, Well, Strain, DesignElement

class PlateForm(forms.Form):
	name = forms.CharField()
	project = forms.ModelChoiceField(queryset=Project.objects.all(),empty_label=None)
	experimenter = forms.ModelChoiceField(queryset=Experimenter.objects.all(),empty_label=None)
	date = forms.DateField(widget=forms.SelectDateWidget())
	dataFile = forms.FileField()

class PlateDesignForm(forms.Form):

    strain = forms.ModelChoiceField(Strain.objects.all())
    design_0 = forms.CharField(required=False)
    value_0 = forms.CharField(required=False)
    design_1 = forms.CharField(required=False)
    value_1 = forms.CharField(required=False)
    design_2 = forms.CharField(required=False)
    value_2 = forms.CharField(required=False)
    design_3 = forms.CharField(required=False)
    value_3 = forms.CharField(required=False)
    design_4 = forms.CharField(required=False)
    value_4 = forms.CharField(required=False)
    design_5 = forms.CharField(required=False)
    value_5 = forms.CharField(required=False)
    design_6 = forms.CharField(required=False)
    value_6 = forms.CharField(required=False)
    design_7 = forms.CharField(required=False)
    value_7 = forms.CharField(required=False)
    design_8 = forms.CharField(required=False)
    value_8 = forms.CharField(required=False)
    design_9 = forms.CharField(required=False)
    value_9 = forms.CharField(required=False)
    wells = forms.CharField()

class WellsReplicateForm(forms.Form):

    def __init__(self,*args,**kwargs):
        wells = kwargs.pop('wells')
        super(WellsReplicateForm,self).__init__(*args,**kwargs)

        for w in wells:
            self.fields['%d'%w.number] = forms.IntegerField(min_value=0,initial=w.biologicalReplicate)


class WellReplicateForm(forms.Form):

    biologicalReplicate = forms.IntegerField(label="Biological Replicate",min_value=0)


