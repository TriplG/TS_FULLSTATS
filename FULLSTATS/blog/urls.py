from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('sort', Sort.as_view(), name='sort'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/rating/', ChangeRating.as_view(), name='rating'),
    path('post/<slug:post_slug>/new_rating/', ChangeNewRating.as_view(), name='change_new_rating'),

]
