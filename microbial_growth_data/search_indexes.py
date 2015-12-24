"""Search index used by the haystack package"""

from haystack import indexes
from .models import ExperimentalDesign, Strain


class ExperimentalDesignIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    strain = indexes.CharField(model_attr='strain')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return ExperimentalDesign

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class StrainIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # strain = indexes.CharField(model_attr='strain')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Strain

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()