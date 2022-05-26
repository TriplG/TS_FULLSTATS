from django.urls import path
from .views import *

# git push -u origin main

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('sort', Sort.as_view(), name='sort'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/rating/', ChangeRating.as_view(), name='rating'),
    path('post/<slug:post_slug>/new_rating/', ChangeNewRating.as_view(), name='change_new_rating'),
    path('post/<slug:post_slug>/like/', Like.as_view(), name='like'),
    path('post/<slug:post_slug>/dislike/', Dislike.as_view(), name='dislike'),
    path('my_likes/', MyLikes.as_view(), name='my_likes'),
    path('post/<slug:post_slug>/unmark/', Unmark.as_view(), name='unmark'),
    path('search/', SearchView.as_view(), name='search'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add_registration/', AddRegistration.as_view(), name='add_registration'),
]