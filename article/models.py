import misaka
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.utils import timezone
from django.utils.text import slugify
from django_resized import ResizedImageField

User = get_user_model()


class Category(models.Model):
	category_name = models.CharField(max_length=255)

	def __str__(self):
		return self.category_name


def static_folder(instance, filename):
	return '/'.join([instance.category.category_name,
					 str(instance.created_date.year) + str(instance.created_date.month) + str(
						 instance.created_date.day), instance.slug, filename])


# return '/'.join([instance.date_build., str(instance.date_build.year), str(instance.date_build.month), filename])

class ArticleText(models.Model):
	user = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	slug = models.SlugField(unique=True, allow_unicode=True)
	image = ResizedImageField(null=True, blank=True, upload_to=static_folder, size=[1920, 1080], keep_meta=True,
							  quality=90)
	publish = models.BooleanField(default=False)
	publish_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now_add=True)
	article_text = RichTextField(blank=True, default='')
	article_text_html = models.TextField(editable=False, default="", blank=True)

	def save(self, *args, **kwargs):
		self.modified_date = timezone.now()
		self.slug = slugify(self.title)
		self.article_text_html = misaka.html(self.article_text)
		super(ArticleText, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Entry"
		verbose_name_plural = "Entries"
		ordering = ["-created_date"]
