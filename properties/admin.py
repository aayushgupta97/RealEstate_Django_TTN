from django.contrib import admin
from accounts.models import Users
# Register your models here.
from .models import Property

admin.site.register(Property)