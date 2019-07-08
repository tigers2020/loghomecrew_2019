import os

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import ImageField, get_thumbnail


# Create your models here.


class Location(models.Model):
    state = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return '[' + self.state + ']' + self.name

    class Meta:
        ordering = ["-name"]


def image_folder(instance, filename):
    path = os.path.join(str(instance.date_build.year), instance.location.state, filename)
    return path


class BuildingImages(models.Model):
    image = ImageField(upload_to=image_folder)
    published = models.BooleanField(default=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_build = models.DateTimeField(blank=True, editable=False)
    date_build_year = models.CharField(max_length=32, null=True, blank=True, editable=False)

    def __str__(self):
        return '{} - {}'.format(str(self.date_build), self.get_title())

    def get_title(self):
        return self.location.name

    def image_tag(self):
        im = get_thumbnail(self.image, '250x125', crop='center')
        return mark_safe('<img src="%s" width=250px />' % im.url)

    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.location.name

        if self.date_build is None or self.date_build == "":
            image_exif = get_exif(self.image)

            # saving datas
            if 'DateTimeOriginal' in image_exif:
                created_date = datetime.strptime(image_exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            elif "DateTimeDigitized" in image_exif:
                created_date = datetime.strptime(image_exif['DateTimeDigitized'], '%Y:%m:%d %H:%M:%S')
            else:
                created_date = datetime.now()
            self.date_build = created_date
            self.date_build_year = created_date.year

        super(BuildingImages, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_build']


class LogHomeModel(models.Model):
    title = models.CharField(max_length=64)
    bedroom = models.IntegerField(default=1)
    bathroom = models.FloatField(default=1)
    story = models.FloatField(default=1)
    wide = models.FloatField()
    deep = models.FloatField()
    description = RichTextField(blank=True, default="")

    def __str__(self):
        return self.title


class Project(models.Model):
    year = models.IntegerField(default=2000)
    title = models.CharField(max_length=64)
    model = models.ForeignKey(LogHomeModel, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    images = models.ManyToManyField(BuildingImages)
    description = RichTextField(blank=True)
    date = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def get_images(self):
        return "\n".join([i.image.name for i in self.images.all()])

    def get_image_url(self):
        return [i.image for i in self.images.all()]

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
