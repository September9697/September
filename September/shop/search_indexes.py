import datetime
from haystack import indexes
from .models import Category,Product

class NameIndex(indexes.SearchIndex,indexes.Indexable):
	text=indexes.CharField(document=True,use_template=True)
	#???????????

	nm=indexes.CharField(model_attr='name')

	def get_model(self):
		return Product

	# def index_queryset(self,using=None):
