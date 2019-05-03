from django.db import models
from django.contrib import auth
from django.utils import timezone


# Create your models here.

class User(auth.get_user_model(), auth.models.PermissionsMixin):
	def __str__(self):
		return "*{}".format(self.username)
