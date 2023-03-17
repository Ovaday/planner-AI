# example/urls.py
from django.urls import path

from example.views import index, base


urlpatterns = [
    path('', index),
    path('base', base),
]