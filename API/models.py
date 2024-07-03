from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
    filepath = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        if not self.filepath:
            self.filepath = self.username
        super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)


class File(models.Model):
    name = models.CharField(max_length=100)
    # path = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', to_field='username')
    
    # def save (self, *args, **kwargs):
    #     if not self.path:
    #         self.path = self.name
    #     super().save(*args, **kwargs)
