"""loghomecrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.generic import RedirectView

from article import views as article_views
from galleries import views as gallery_views
from home import views as home_views
from home.views import SiteSitemap
from loghomecrew import settings

sitemaps = {
    'site': SiteSitemap,
}

urlpatterns = [
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url('sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/main/favicon/favicon.ico')),
    url(r'^$', home_views.IndexView.as_view(), name='index_view'),
    url(r'^aboutus/$', article_views.AboutUsView.as_view(), name='about_us'),
    url(r'^faq/$', article_views.FaQView.as_view(), name='faq_view'),
    url(r'^galleries$', gallery_views.GalleriesIndexView.as_view(), name='galleries_index'),
    # url(r'^galleries/', include('galleries.urls')),
    # url(r'^article/', include('article.urls')),
    url(r'^contact_us/', home_views.contact, name='contact_us'),
    url(r'^contact_us/send_failed', home_views.contact_failed, name='failed'),
    url(r'^contact_us/success', home_views.contact_success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
