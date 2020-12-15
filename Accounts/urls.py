from django.urls import path
from . import views
from django.conf.urls import include,url

urlpatterns = [
    url('^$',views.homepage, name = 'homepage'),
    path('signup/',views.signup, name = 'signup'),
    path('login/', views.loginpage, name='loginpage'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    #path('delete/', views.delete, name='delete'),
]