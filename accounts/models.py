from django.contrib.auth.models import AbstractUser
from django.db import models

#
# class Seller(models.Model):
#     name = models.CharField(max_length=200)
#     photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
#     description = models.TextField(blank=True)
#     phone = models.CharField(max_length=20)
#     email = models.CharField(max_length=50)
#     is_seller = models.BooleanField(default=False)


class Users(AbstractUser):
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=20)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username

