from django.contrib import admin
from Accounts.models import Users, Books, Ratings, Overall_Ratings

admin.site.register(Users)
admin.site.register(Books)
admin.site.register(Ratings)
admin.site.register(Overall_Ratings)