from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from account import forms


class SignUp(CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy('login')
	template_name = 'accounts/signup.html'
