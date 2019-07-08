import os
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from django.conf import settings
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


def change_image_location(modeladmin, request, queryset):
    for instance in queryset:
        if instance.image:
            initial_path = instance.image.path
            file_name = os.path.basename(instance.image.name)
            new_rel_path = os.path.join(str(instance.date_build.year), instance.location.state, file_name)
            new_abs_path = os.path.join(settings.MEDIA_ROOT, new_rel_path)
            print('initial path', initial_path)
            print('new path: ', new_abs_path)
            if os.path.isfile(new_abs_path):
                print("File with that name already exists, skipping!")
            else:
                try:
                    os.rename(initial_path, new_abs_path)
                except Exception as exc:
                    # handle OS errors if needed
                    raise exc
                else:
                    instance.image.name = new_rel_path
                    instance.save()


def apply_to_publish(modeladmin, request, queryset):
    for instance in queryset:
        if instance.published:
            instance.published = False
        else:
            instance.published = True

        instance.save()
    apply_to_publish.short_description = "publish image"


def set_date_time_from_image(modeladmin, request, queryset):
    for instance in queryset:
        image_exif = get_exif(instance.image)
        print("image_exif", image_exif)
        # saving datas
        created_date = datetime.now()
        if 'DateTimeOriginal' in image_exif:
            created_date = datetime.strptime(image_exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        elif "DateTimeDigitized" in image_exif:
            created_date = datetime.strptime(image_exif['DateTimeDigitized'], '%Y:%m:%d %H:%M:%S')

        print("set image date:", created_date)
        instance.date_build = created_date
        instance.date_build_year = created_date.year
        instance.save()
        set_date_time_from_image.short_description = "set the date time"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'location', 'get_images', 'description', 'date', 'published',)
    ordering = ('-year',)



class GalleriesAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("title", "image_tag", "location", "published", "date_build", "date_build_year",)
    ordering = ('-date_build',)
    readonly_fields = ('image_tag',)
    list_filter = ('category', 'date_build_year')
    actions = [apply_to_publish, set_date_time_from_image, change_image_location]


class LocationAdmin(admin.ModelAdmin):
    list_display = ('state', 'name')
    ordering = ('state',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.BuildingImages, GalleriesAdmin)
admin.site.register(models.Location, LocationAdmin)
