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
    # designElements = forms.ModelMultipleChoiceField(DesignElement.objects.all(),label="Design Elements",required=False)
    wells = forms.CharField()