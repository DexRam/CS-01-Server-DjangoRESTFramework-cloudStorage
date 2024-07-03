from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
    filepath = models.CharField(max_length=100, blank=True)
    


class File(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', to_field='username')
