import datetime
from django.contrib.sitemaps import Sitemap
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from article.models import ArticleText
from galleries.models import BuildingImages
# Create your views here.
from home.forms import ContactForm
from loghomecrew import settings

import itertools


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        images = BuildingImages.objects.filter(published=True).order_by('date_build').order_by('-location')
        years = set()
        img = {}
        for image in images:
            years.add(image.date_build_year)
        years = list(years)
        years.sort(reverse=True)
        for year in years:
            img.update({year: images.filter(date_build_year=year)})

        text = ArticleText.objects.filter(publish=True)

        features = text.filter(category=1)
        testimonials = text.filter(category=3)
        services = text.filter(category=5)


        context['years'] = years
        context['images'] = img

        context['features'] = features
        context['testimonials'] = testimonials
        context['services'] = services
        return context


class ContactUsView(generic.TemplateView):
    template_name = 'home/contact_us.html'


def contact(request):
    thank_you = {}
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            from_email = form.cleaned_data.get("email")
            feedback = form.cleaned_data.get('feed_back')

            subject = '[%s]'.format(feedback) + form.cleaned_data.get("subject") + "-" + first_name + " " + last_name
            body_message = form.cleaned_data.get("message")

            if send_mail(subject, body_message, from_email, recipient_list=[settings.DEFAULT_FROM_EMAIL],
                         html_message=body_message):
                print("sending email success")
                thank_you = {"You have successfully submitted. We will contact you in short time."}
            else:
                print('sending email failed')

    return render(request, "home/contact_us.html", {'form': form, 'success': thank_you})


def contact_success(request):
    return HttpResponse("Success! Thank you for your message")


def contact_failed(request):
    return HttpResponse("Send Email Failed")


class SiteSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    lastmod = datetime.datetime.now()

    def items(self):
        return ['index_view', 'about_us', 'galleries_index', 'faq_view', 'contact_us']

    def location(self, obj):
        return reverse(obj)
