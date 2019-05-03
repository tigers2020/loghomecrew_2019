from django.contrib import admin
from django.utils.html import format_html

from . import models


# Register your models here.


def apply_to_publish(queryset):
	for published in queryset:
		if published.published:
			published.published = False
		else:
			published.published = True

		published.save()

	apply_to_publish.short_description = "publish image"

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'image', 'description', 'date', 'published', )

class GalleriesAdmin(admin.ModelAdmin):
	list_display = ("title", "image_tag", "location", "published", "imgorigsize", "date_build", "date_build_year",)
	ordering = ('date_build',)
	readonly_fields = ('image_tag',)
	actions = [apply_to_publish]


class LocationAdmin(admin.ModelAdmin):
	list_display = ('state', 'name')
	ordering = ('state',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.BuildingImages, GalleriesAdmin)
admin.site.register(models.Location, LocationAdmin)
