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
from django.utils.text import slugify
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
    return '{}/{}/{}/{}'.format(instance.location.state, instance.date_build.year, instance.date_build.month, filename)


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    image = models.ImageField(blank=True)
    description = RichTextField(blank=True)
    date = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


class BuildingImages(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = ImageField(upload_to=image_folder)
    published = models.BooleanField(default=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_build = models.DateTimeField(blank=True, editable=False)
    date_build_year = models.CharField(max_length=32, null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    def image_tag(self):
        im = get_thumbnail(self.image, '200x100', crop='center')
        return mark_safe('<img src="/media/%s" width=200px />' % im)

    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.location.name

        if self.date_build is None or self.date_build == "":
            image_exif = get_exif(self.image)

            # saving datas
            if 'DateTime' in image_exif:
                created_date = datetime.strptime(image_exif['DateTime'], '%Y:%m:%d %H:%M:%S')
                self.date_build = created_date
                self.date_build_year = created_date.year

        super(BuildingImages, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_build']
