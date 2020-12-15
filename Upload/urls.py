from . import views
from django.urls import path
from django.conf.urls import include,url


urlpatterns = [
    url(r'^newusr/$', views.adduser, name='addusr'),
    url(r'^authusr/$', views.auth_user, name='auth_user'),
    #url(r'^authusr/homepage/', views.top_rated, name='top_rated'),
]
