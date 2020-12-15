from . import views
from django.urls import path, re_path
from django.conf.urls import include,url


urlpatterns = [
    url(r'^$', views.searchn, name='searchn'),
]