from django.db import models
from django.contrib.auth.models import AbstractUser

class Users2(models.Model):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=125)
    password = models.CharField(max_length=125)

class Test(models.Model):
    text = models.CharField(max_length=140)
