from django.conf.urls import url

from article import views
from . import models

app_name = 'article_app'

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='article_index'),
	# url(r'^aboutus/$', views.AboutUsView.as_view(), name='about_us'),
	# url(r'^faq/$', views.FaQView.as_view(), name='faq_view'),
]
