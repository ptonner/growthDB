from django import forms
from .models import Project, Experimenter

class PlateForm(forms.Form):
	name = forms.CharField()
	project = forms.ModelChoiceField(queryset=Project.objects.all(),empty_label=None)
	experimenter = forms.ModelChoiceField(queryset=Experimenter.objects.all(),empty_label=None)
	date = forms.DateField(widget=forms.SelectDateWidget())
	dataFile = forms.FileField()

	def send_email(self):
		# send email using the self.cleaned_data dictionary
		pass