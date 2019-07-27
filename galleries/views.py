from braces.views import SelectRelatedMixin
from django.views import generic

from .models import BuildingImages, Location


class GalleriesIndexView(generic.ListView):
	model = BuildingImages

	def get_queryset(self):
		queryset = super(GalleriesIndexView, self).get_queryset()

		return queryset
	def get_context_data(self, **kwargs):
		context = super(GalleriesIndexView, self).get_context_data(**kwargs)
		location = BuildingImages.objects.order_by().values('location').distinct()
		locations = []
		for name in location:
			locations.append(Location.objects.get(id=name['location']))
			print(name)

		context['locations'] = locations
		return context



class GalleriesDetailView(SelectRelatedMixin, generic.ListView):
	model = BuildingImages
	select_related = ('location',)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
