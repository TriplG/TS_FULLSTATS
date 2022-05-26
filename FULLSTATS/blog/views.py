from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.urls import reverse_lazy


from .models import *
from .forms import *

from django.views.generic.edit import FormView



class Home(ListView):
    # Представление главной страницы со всеми статьями
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    queryset = Article.objects.all().order_by('-pk')

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     object_list = Article.objects.filter(
    #         slug__icontains=query
    #     )
    #     return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = SortForm()
        context['title'] = 'Главная страница'
        return context


class Sort(View):
    # Представление отсортированной главной страницы
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
    # Представление конкретной статьи
    model = Article
    template_name = 'blog/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        if f'{self.kwargs["post_slug"]}_rating' in self.request.COOKIES:
            context['rate'] = self.request.COOKIES[f'{self.kwargs["post_slug"]}_rating']
        if f'{self.kwargs["post_slug"]}_liked' in self.request.COOKIES:
            context['liked'] = self.request.COOKIES[f'{self.kwargs["post_slug"]}_liked']
        if f'{self.kwargs["post_slug"]}_disliked' in self.request.COOKIES:
            context['liked'] = self.request.COOKIES[f'{self.kwargs["post_slug"]}_disliked']

        return context


class ChangeRating(View):
    # Представление для изменения рейтинга неавторизованному пользователю в первый раз
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
    # Представление для изменения рейтинга неавторизованному пользователю в последующие разы
    def post(self, request, post_slug):
        try:
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


class Like(View):
    # Представление для возможности поставить лайк неавторизованному пользователю

    def post(self, request, post_slug):
        try:
            response = redirect(f'/post/{post_slug}/')
            response.set_cookie(f'{post_slug}_liked', 1)
            return response
        except ObjectDoesNotExist:
            raise Http404
        return redirect(f'/post/{post_slug}/')


class Dislike(View):
    # Представление для возможности поставить дизлайк неавторизованному пользователю
    def post(self, request, post_slug):
        try:
            response = redirect(f'/post/{post_slug}/')
            response.set_cookie(f'{post_slug}_disliked', -1)
            return response
        except ObjectDoesNotExist:
            raise Http404
        return redirect(f'/post/{post_slug}/')


class MyLikes(View):
    # Представление понравившихся постов для неавторизованных пользователей
    def get(self, request):
        posts = Article.objects.all()
        context = {
            'posts': posts,
            'title': 'Мне понравилось'
        }
        return render(request, 'blog/my_likes.html', context=context)


class Unmark(View):
    # Представление для отмены лайка/дизлайка неавторизованным пользователям
    def post(self, request, post_slug):

        response = redirect(f'/post/{post_slug}/')
        if f'{post_slug}_liked' in request.COOKIES:
            response.delete_cookie(f'{post_slug}_liked')
        if f'{post_slug}_disliked' in request.COOKIES:
            response.delete_cookie(f'{post_slug}_disliked')
        return response


class SearchView(View):
    def get(self, request):
        try:
            print(request.GET.get("q", ""))
            return redirect(f'/post/{request.GET.get("q", "")}/')
        except ObjectDoesNotExist:
            raise Http404
        return redirect('/')


class Registration(View):
    def get(self, request):
        return render(request, 'blog/register.html', {'title': 'Корзина'})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context

    def get_success_url(self):
        return reverse_lazy('index')


class AddRegistration(View):
    def post(self, request):
        create_user = User.objects.create_user(
            request.POST.get('name'), request.POST.get('email'), request.POST.get('password')
        )
        create_user.save()

        print(request.POST)
        return redirect('/login/')
