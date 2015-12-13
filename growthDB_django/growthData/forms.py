from django import forms
from .models import Project, Experimenter, ExperimentalDesign, Well, Strain, DesignElement

class PlateForm(forms.Form):
	name = forms.CharField()
	project = forms.ModelChoiceField(queryset=Project.objects.all(),empty_label=None)
	experimenter = forms.ModelChoiceField(queryset=Experimenter.objects.all(),empty_label=None)
	date = forms.DateField(widget=forms.SelectDateWidget())
	dataFile = forms.FileField()


class PlateDesignForm(forms.Form):
    # def __init__(self, pk, *args, **kwargs):
    #     super(PlateDesignForm, self).__init__(*args, **kwargs)

    #     self.fields['experimentalDesigns'].queryset = 
    #     self.fields['to_user'].queryset = self.fields['to_user'].queryset.exclude(id=current_user.id)

    # experimentalDesign = forms.ModelChoiceField(ExperimentalDesign.objects.all(),empty_label=None)
    # wells = forms.ModelMultipleChoiceField(Well.objects.all(),widget=forms.SelectMultiple(attrs={'size': 200}))

    strain = forms.ModelChoiceField(Strain.objects.all())
    designElements = forms.ModelMultipleChoiceField(DesignElement.objects.all(),label="Design Elements",)
    wells = forms.CharField()