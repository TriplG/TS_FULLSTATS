from django.shortcuts import render
from .models import *


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'blog/index.html', context=context)
