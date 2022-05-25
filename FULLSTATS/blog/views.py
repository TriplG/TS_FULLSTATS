from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View

from .models import *
from .forms import *


def index(request):
    posts = Article.objects.all()
    sort_form = SortForm()
    context = {
        'sort_form': sort_form,
        'posts': posts,
        'title': 'Главная страница'
    }
    return render(request, 'blog/index.html', context=context)


class Home(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = SortForm()
        context['title'] = 'Главная страница'
        return context


class Sort(View):
    def post(self, request):
        sort_form = SortForm(request.POST)
        posts = Article.objects.all()
        if sort_form.is_valid():
            needed_sort = sort_form.cleaned_data.get("sort_form")
            # Изначально посты отсортированы по дате, поэтому проверка для этого поля не нужна.
            if needed_sort == "рейтинг":
                posts = posts.order_by("rating")
        context = {
            'sort_form': sort_form,
            'posts': posts,
            'title': 'Главная страница'
        }
        return render(request, 'blog/index.html', context=context)
