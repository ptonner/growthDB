from __future__ import unicode_literals

from django.db import models

class Plate(models.Model):
	experimenter = models.ForeignKey('Experimenter')
	project = models.ForeignKey('Project')
	date = models.DateField(auto_now_add=True)
	dataFile = models.FileField(upload_to='uploads/%Y/%m/%d/')


class Experimenter(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    dataStarted = models.DateField(auto_now_add=True)


class Well(models.Model):
	experimentalDesign = models.ForeignKey('ExperimentalDesign')

	# these three fields constitute the replicate information
	plate = models.ForeignKey('Plate')
	biologicalReplicate = models.IntegerField(default=0)
	technicalReplicate = models.IntegerField(default=0)

	unique_together = (("plate", "biologicalReplicate","technicalReplicate"),)


class ExperimentalDesign(models.Model):
	strain = models.ForeignKey('Strain')
	designElements = models.ManyToManyField("DesignElement")


class DesignElement(models.Model):
	strain = models.ForeignKey('Design')
	value = models.CharField(max_length=100)


class DesignElement(models.Model):

	 TYPES = (
        ('str', 'str'),
        ('int', 'int'),
        ('float', 'float'),
    )
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=1, choices=TYPES)
	

