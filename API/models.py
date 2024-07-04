import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
    filepath = models.CharField(max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.filepath = f"files/{self.username}/"
        super().save(*args, **kwargs)
    


class File(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', to_field='username', blank=True,)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.file.name = os.path.join(self.owner.filepath, self.file.name)
        super().save(*args, **kwargs)