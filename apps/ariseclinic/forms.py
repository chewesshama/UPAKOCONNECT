#from django import forms
#from django.contrib.auth.forms import (
#    UserCreationForm,
#    AuthenticationForm,
#    PasswordChangeForm,
#)
#from .models import User
#
#
#class LoginForm(AuthenticationForm):
#    username = forms.CharField(
#        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
#    )
#
#    password = forms.CharField(
#        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
#    )
#
#    username.label = "Username"
#    username.label_classes = ["text-danger"]