from django.contrib import admin

from .models import ExperimentalDesign, DesignElement, Design, Project, Experimenter, Well, Plate, Strain

admin.site.register(ExperimentalDesign)
admin.site.register(DesignElement)
admin.site.register(Design)
admin.site.register(Project)
admin.site.register(Experimenter)
admin.site.register(Well)
admin.site.register(Plate)
admin.site.register(Strain)