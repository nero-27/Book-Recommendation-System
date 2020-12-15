from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from Accounts.models import Users
from Accounts.models import Books
from Accounts.models import Ratings
from Accounts.models import Overall_Ratings
from Upload.views import Users_upload, books_upload, ratings_upload, Overall_Ratings_upload


urlpatterns = [
    path('admin/', admin.site.urls),
    url('^',include('Accounts.urls')),
    url('^description/',include('Description.urls'), name="description"),
    url('^searchn/',include('Search.urls'), name="searchn"),
    url('^rate/',include('Rate.urls'), name="rate"),
    path('upload-users-csv/', Users_upload, name="Users_upload"),
    path('upload-books-csv/', books_upload, name="books_upload"),
    path('upload-ratings-csv/', ratings_upload, name="ratings_upload"),
    path('upload-overall-ratings-csv/', Overall_Ratings_upload, name="Overall_Ratings_upload"),
]
