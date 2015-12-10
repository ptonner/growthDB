from __future__ import unicode_literals

from django.db import models

class Plate(models.Model):
	experimenter = models.ForeignKey('Experimenter')
	project = models.ForeignKey('Project')
	name = models.CharField(max_length=200,unique=True)
	date = models.DateField(auto_now_add=True)
	dataFile = models.FileField(upload_to='uploads/%Y/%m/%d/')

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

	# these three fields constitute the replicate information
	plate = models.ForeignKey('Plate')
	biologicalReplicate = models.IntegerField(default=0)
	technicalReplicate = models.IntegerField(default=0)

	unique_together = (("plate", "biologicalReplicate","technicalReplicate"),)

	def __str__(self):
		return "%s (%s) - (%s)" % (self.plate, self.number, self.experimentalDesign)


class ExperimentalDesign(models.Model):
	strain = models.ForeignKey('self')
	designElements = models.ManyToManyField("DesignElement")

	def __str__(self):
		s = ",".join(str(x) for x in self.designElements)

		return "%s - %s" % (self.strain,s)


class DesignElement(models.Model):
	design = models.ForeignKey('Design')
	value = models.CharField(max_length=100)

	def __str__(self):
		return self.design, self.value


class Design(models.Model):

	TYPES = (
		('str', 'str'),
		('int', 'int'),
		('float', 'float'),
	)

	name = models.CharField(max_length=60)
	description = models.CharField(max_length=1000)
	type = models.CharField(max_length=1, choices=TYPES)

	def __str__(self):
		return self.name


