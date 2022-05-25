from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('sort', Sort.as_view(), name='sort'),

]
