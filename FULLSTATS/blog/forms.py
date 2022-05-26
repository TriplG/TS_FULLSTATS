from django import forms
from .models import *


class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(label='Сортировать:',
                                       choices=[
                                           ('дата', 'По дате'),
                                           ('рейтинг', 'По рейтингу'),
                                           ('просмотры', 'По просмотрам')
                                           ]
                                       )
