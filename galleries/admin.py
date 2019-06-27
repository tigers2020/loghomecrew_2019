from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from . import models


# Register your models here.


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def apply_to_publish(modeladmin, request, queryset):
    for published in queryset:
        if published.published:
            published.published = False
        else:
            published.published = True

        published.save()
    apply_to_publish.short_description = "publish image"


def set_date_time_from_image(modeladmin, request, queryset):
    for query in queryset:
        if query.date_build == None:
            image_exif = get_exif(query.image)

            # saving datas
            if 'DateTime' in image_exif:
                created_date = datetime.strptime(image_exif['DateTime'], '%Y:%m:%d %H:%M:%S')
                print("set image date:", created_date)
                query.date_build = created_date
                query.date_build_year = created_date.year
        query.save()
        set_date_time_from_image.short_description = "set the date time"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description', 'date', 'published',)


class GalleriesAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("title", "image_tag", "location", "published", "date_build", "date_build_year",)
    ordering = ('-date_build',)
    readonly_fields = ('image_tag',)
    list_filter = ('location', 'date_build_year')
    actions = [apply_to_publish, set_date_time_from_image]


class LocationAdmin(admin.ModelAdmin):
    list_display = ('state', 'name')
    ordering = ('state',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.BuildingImages, GalleriesAdmin)
admin.site.register(models.Location, LocationAdmin)
