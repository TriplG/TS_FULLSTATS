from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Article(models.Model):
    title_translate = models.CharField(verbose_name='Название статьи на английском', max_length=50)
    title = models.CharField(verbose_name='Название статьи', max_length=50)
    author = models.CharField(verbose_name='Автор', max_length=25)
    summary = models.CharField(verbose_name='Краткое содержание', max_length=250)
    content = models.TextField(verbose_name='Содержание')
    num_of_views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)
    favorites = models.BooleanField(verbose_name='В избранном', default=False)
    my_mark = models.IntegerField(verbose_name='Моя оценка', default=0,
                                  validators=[
                                      MinValueValidator(-1),
                                      MaxValueValidator(1)
                                  ]
                                  )
    rating = models.IntegerField(verbose_name='Рейтинг', null=True, blank=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
