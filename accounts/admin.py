from django.contrib import admin
from .models import Users
# Register your models here.


class UsersAdmin(admin.ModelAdmin):

    model = Users
    list_display = ['first_name', 'last_name', 'email', 'username',]
    list_filter = ['is_seller',]


admin.site.register(Users, UsersAdmin)