from django.contrib import admin
from accounts.models import Users
# Register your models here.
from .models import Property
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller')

admin.site.register(Property, PropertyAdmin)