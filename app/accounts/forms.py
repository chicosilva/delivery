# coding=utf-8

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from django.contrib.auth.hashers import check_password, make_password


class FormLogin(forms.Form):
    password = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput(), required=True)
    email = forms.EmailField(label="e-mail", required=True)

class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class UserEditAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff']

class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'is_active', 'is_staff', 'password']

    def clean_password(self):
        return make_password(self.cleaned_data['password'])
