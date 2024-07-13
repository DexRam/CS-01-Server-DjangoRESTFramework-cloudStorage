import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    file_path = models.CharField(max_length=100, blank=True, editable=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.file_path = os.path.join("files", self.username)
        if self.is_superuser:
            self.is_admin = True
        super().save(*args, **kwargs)


class File(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="files",
        to_field="username",
        blank=True,
    )
    uploaded_at = models.DateTimeField(default=timezone.now)
    downloaded_at = models.DateTimeField(blank=True, null=True)
    share_link = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=100, blank=True)

    def file_upload_path(self, filename):
        return f"files/{self.owner.username}/{filename}"

    file = models.FileField(upload_to=file_upload_path)

    def generate_share_link(self):
        return str(uuid.uuid4())