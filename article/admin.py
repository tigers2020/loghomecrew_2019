from django import forms
from django.contrib import admin
from django.utils import timezone
from article.models import ArticleText
from ckeditor.widgets import CKEditorWidget
from . import models


class ArticleAdminForm(forms.ModelForm):
	article_text = forms.CharField(widget=CKEditorWidget())




def publishing(modeladmin, request, queryset):
	for publish in queryset:
		publish.publish = True
		publish.publish_date = timezone.now()
		publish.save()
	publishing.short_description = "publishing"


def unpublishing(modeladmin, request, queryset):
	for publish in queryset:
		publish.publish = False
		publish.publish_date = None
		publish.save()
	unpublishing.short_description = "unpublishing"


class ArticleModelAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "created_date", "modified_date", "publish", "publish_date")
	prepopulated_fields = {"slug": ("title",)}
	list_editable = ['publish']
	actions = [publishing, unpublishing]
	form = ArticleAdminForm
	search_fields = ["title", "article_text"]

	class Meta:
		model = ArticleText

class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'category_name')
	form= ArticleAdminForm
	search_fields = ['category_name']

# Register your models here.

admin.site.register(models.ArticleText, ArticleModelAdmin)
admin.site.register(models.Category, CategoryModelAdmin)
