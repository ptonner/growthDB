from __future__ import unicode_literals

from django.db import models

class Plate(models.Model):
	experimenter = models.ForeignKey('Experimenter')
	project = models.ForeignKey('Project')
	name = models.CharField(max_length=200,unique=True)
	date = models.DateField(auto_now_add=True)
	dataFile = models.FileField(upload_to='uploads/%Y/%m/%d/')
	cleanedData = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True)
	image = models.FileField(upload_to='uploads/plate-images/',null=True)
	changed = models.BooleanField(default=True)

	def experimentalDesigns(self,):
		return ExperimentalDesign.objects.filter(well__in=self.well_set.all()).distinct()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('plate', kwargs={'pk': self.pk})

class Experimenter(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=20,unique=True)
	description = models.CharField(max_length=1000)
	dataStarted = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.name

class Well(models.Model):
	experimentalDesign = models.ForeignKey('ExperimentalDesign',null=True)
	number = models.IntegerField(default=0)

	# these two fields constitute the replicate information
	plate = models.ForeignKey('Plate')
	biologicalReplicate = models.IntegerField(default=0)

	def __str__(self):
		return "%s (%s) - (%s)" % (self.plate, self.number, self.experimentalDesign)

class Strain(models.Model):
	parent = models.ForeignKey('self',null=True,blank=True, related_name='subarticles')
	name = models.CharField(max_length=20)

	def __str__(self):
		if self.parent:
			return "%s ( %s )" % (self.name, self.parent.name)
		else:
			return "%s ( %s )" % (self.name, None)


class ExperimentalDesign(models.Model):
	strain = models.ForeignKey('Strain')
	designElements = models.ManyToManyField("DesignElement",blank=True)

	# class Meta:
	# 	unique_together = (("strain", "designElements"),)

	def plates(self,):
		return Plate.objects.filter(well__in=self.well_set.all()).distinct()

	def designElementString(self):
		s = ", ".join(str(x) for x in self.designElements.all())
		return s

	def __str__(self):
		# s = ",".join(str(x) for x in self.designElements.all())

		return "%s - %s" % (self.strain.name,self.designElementString())


class DesignElement(models.Model):
	design = models.ForeignKey('Design')
	value = models.CharField(max_length=100)

	def __str__(self):
		return "%s: %s" % (self.design, self.value)

class Design(models.Model):

	TYPES = (
		('str', 'str'),
		('int', 'int'),
		('float', 'float'),
	)

	name = models.CharField(max_length=60)
	description = models.CharField(max_length=1000)
	type = models.CharField(max_length=5, choices=TYPES)

	def __str__(self):
		return self.name


