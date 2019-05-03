import os
from django.db import models
from PIL import Image
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.core.files.base import ContentFile
from datetime import datetime
from ckeditor.fields import RichTextField


# Create your models here.
from io import BytesIO

from loghomecrew import settings


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
	return settings.MEDIA_URL.join([instance.location.state, str(instance.date_build.year), str(instance.date_build.month), filename])


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


class BuildingImages(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=255, blank=True, null=True)
	image = ResizedImageField(null=True, blank=True, upload_to=image_folder, size=[1280, 720], keep_meta=True,
							  quality=90)
	thumb_image = models.ImageField(upload_to=image_folder, editable=False, blank=True)
	description = RichTextField(blank=True, null=True)
	imgorigsize = models.IntegerField(editable=False, null=True, blank=True)
	published = models.BooleanField(default=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	date_build = models.DateField(auto_created=False, auto_now=False, auto_now_add=False, blank=True, editable=False)
	date_build_year = models.CharField(max_length=32, null=True, blank=True, editable=False)

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="/media/%s" width=160px />' % self.thumb_image)

	image_tag.allow_tags = True

	def save(self, *args, **kwargs):

		if not self.pk:
			if not self.save_thumbnail():
				raise Exception('Could not create thumbnail - is the file type valid?')
		if not self.title:
			self.title = self.location.name

		super(BuildingImages, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-date_build']

	def save_thumbnail(self):
		im = Image.open(self.image)
		image_size = self.image.size
		im.thumbnail((320, 320), Image.ANTIALIAS)
		image_exif = im._getexif()
		created_date = datetime.strptime(image_exif[36867], '%Y:%m:%d %H:%M:%S')
		print(created_date)

		thumb_name, thumb_extension = os.path.splitext(self.image.name)
		thumb_extension = thumb_extension.lower()
		thumb_filename = thumb_name + "_thumb" + thumb_extension

		if thumb_extension in ['.jpg', '.jpeg']:
			FTYPE = 'JPEG'
		elif thumb_extension == '.gif':
			FTYPE = 'GIF'
		elif thumb_extension == '.png':
			FTYPE = '.PNG'
		else:
			return False

		temp_thumb = BytesIO()
		im.save(temp_thumb, FTYPE)
		temp_thumb.seek(0)

		# saving datas

		self.imgorigsize = image_size
		self.date_build = created_date
		self.date_build_year = created_date.year
		self.thumb_image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
		temp_thumb.close()

		return True
