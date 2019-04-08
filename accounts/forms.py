from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users


class User_Registration(UserCreationForm):
    class meta(UserCreationForm):
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'description', 'phone',
                  'is_seller', 'photo', )


