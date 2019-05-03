
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from . import views

app_name = 'galleries_app'
urlpatterns = [
	# url(r'^$', views.GalleriesIndexView.as_view(), name='galleries_index'),
	url(r'^(?P<year>[\d]+)/(?P<pk>[-\w]+)/$', views.GalleriesDetailView.as_view(), name='galleries_detail')

]

