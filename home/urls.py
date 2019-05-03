from django.conf.urls import url

from loghomecrew import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^$', views.IndexView.as_view(), name='main_index'),

              ]

