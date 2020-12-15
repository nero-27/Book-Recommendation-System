from . import views
from django.urls import path, re_path
from django.conf.urls import include,url


urlpatterns = [
    path('', views.rate, name='rate'),
]