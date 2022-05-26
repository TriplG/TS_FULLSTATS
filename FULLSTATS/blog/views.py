from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import *
from .forms import *


# def index(request):
#     posts = Article.objects.all()
#     sort_form = SortForm()
#
#     context = {
#         'sort_form': sort_form,
#         'posts': posts,
#         'title': 'Главная страница'
#     }
#     return render(request, 'blog/index.html', context=context)


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
            elif needed_sort == "просмотры":
                posts = posts.order_by("num_of_views")
        context = {
            'sort_form': sort_form,
            'posts': posts,
            'title': 'Главная страница'
        }
        return render(request, 'blog/index.html', context=context)


class ShowPost(DetailView):
    model = Article
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        if f'{self.kwargs["post_slug"]}_rating' in self.request.COOKIES:
            context['rate'] = self.request.COOKIES[f'{self.kwargs["post_slug"]}_rating']

        return context


class ChangeRating(View):
    def post(self, request, post_slug):
        try:
            if f'{post_slug}_rating' in request.COOKIES:
                redirect(f'/post/{post_slug}/')
            else:
                art = Article.objects.get(slug=post_slug)
                if RatingArticle.objects.filter(article_rating=art) in RatingArticle.objects.all():
                    rating = RatingArticle.objects.get(article_rating=art)
                    rating.total_amount += int(request.POST.get('num'))
                    rating.qty += 1
                    rating.save()
                else:
                    rating = RatingArticle.objects.create(
                        article_rating=art,
                        total_amount=int(request.POST.get('num')),
                        qty=1,
                    )

                art.rating = rating.total_amount/rating.qty
                art.save()
                # if NotAuthUser.objects.filter(coocies=art) in NotAuthUser.objects.all():
                #     not_auth_user = RatingArticle.objects.create(
                #         delivered_rating=request.POST.get('num'),
                #         coocies=post_slug,
                #     )
                response = redirect(f'/post/{post_slug}/')
                response.set_cookie(f'{post_slug}_rating', request.POST.get('num'))
                return response
        except ObjectDoesNotExist:
            raise Http404
        return redirect(f'/post/{post_slug}/')


class ChangeNewRating(View):
    def post(self, request, post_slug):
        try:
            # if f'{post_slug}_rating' in request.COOKIES:
            #     redirect(f'/post/{post_slug}/')
            # else:
            art = Article.objects.get(slug=post_slug)
            rating = RatingArticle.objects.get(article_rating=art)
            rating.total_amount += int(request.POST.get('num_new')) - int(request.COOKIES[f'{post_slug}_rating'])
            rating.save()

            art.rating = rating.total_amount/rating.qty
            art.save()
            response = redirect(f'/post/{post_slug}/')
            response.set_cookie(f'{post_slug}_rating', request.POST.get('num_new'))
            return response
        except ObjectDoesNotExist:
            raise Http404
        return redirect(f'/post/{post_slug}/')
