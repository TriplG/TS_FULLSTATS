from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Article(models.Model):
    slug = models.SlugField(verbose_name='Название статьи на английском', max_length=50, default='fd')
    title = models.CharField(verbose_name='Название статьи', max_length=50)
    author = models.CharField(verbose_name='Автор', max_length=25)
    summary = models.CharField(verbose_name='Краткое содержание', max_length=250)
    content = models.TextField(verbose_name='Содержание')
    num_of_views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    favorites = models.BooleanField(verbose_name='В избранном', default=False)
    rating = models.DecimalField(verbose_name='Рейтинг', null=True, blank=True, max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class RatingArticle(models.Model):
    article_rating = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='Статья')
    qty = models.PositiveIntegerField(verbose_name='Количество измнений рейтинга', default=0)
    total_amount = models.PositiveIntegerField(verbose_name='Общая сумма оценок', null=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'Рейтинг статьи {self.article_rating}'


# class NotAuthUser(models.Model):
#     coocies_rating = models.CharField(verbose_name='Куки', max_length=250)
#     delivered_rating = models.PositiveIntegerField(verbose_name='Поставленный рейтинг', null=True, blank=True)
#     coocies_mark = models.CharField(verbose_name='Куки', max_length=250)
#     my_mark = models.IntegerField(verbose_name='Оценка', default=0,
#                                   validators=[
#                                       MinValueValidator(-1),
#                                       MaxValueValidator(1)
#                                   ]
#                                   )





