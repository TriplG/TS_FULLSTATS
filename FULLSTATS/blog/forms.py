from django import forms
from .models import *

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(label='Сортировать:',
                                       choices=[
                                           ('дата', 'По дате'),
                                           ('рейтинг', 'По рейтингу'),
                                           ('просмотры', 'По просмотрам')
                                           ]
                                       )


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

