from django.shortcuts import render
from django.http import HttpResponse
from Accounts.models import Books

# Create your views here.
def searchn(request):
    if request.session.has_key('uid'):
        query = request.POST['search'].lower()
        print(query)
        all_books = Books.objects.all()
        context ={}
        found = 0
        context['cart'] = []
        for book in all_books:
            if query == book.Book_Title.lower() or query == book.Book_Author.lower():
                cart = Cart()
                found=1
                cart.Book_Title = book.Book_Title
                cart.Book_Author = book.Book_Author
                cart.Image_URL_M = book.Image_URL_M
                cart.Book_Cost = book.Book_Cost
                cart.Publisher = book.Publisher
                cart.Synopsis = book.Synopsis
                cart.ISBN = book.ISBN
                context['cart'].append(cart)
                print("Found!!--> Book Title:",book.Book_Title," And Author: ",book.Book_Author)
        if found == 1:
            return render(request, 'searchresults.html', context )
        else:
            return render(request, 'nosearchresults.html', context)
    return render(request, 'login.html', {})

class Cart(object):
    model = Books

def searchi(request):
    return HttpResponse("<h1>In Search Image</h1>")


# #Search >>> views.py
#
#
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from Accounts.models import Books
# import difflib
#
# # Create your views here.
# def searchn(request):
#     if request.session.has_key('session_id'):
#         search_query_lowercase = request.POST['search'].lower()
#         print(search_query_lowercase)
#         all_book_objects = Books.objects.all()
#         context ={}
#         book_found = False
#         context['cart'] = []
#         for book in all_book_objects:
#             book_title_lowercase = book.Book_Title.lower()
#             book_author_lowercase = book.Book_Author.lower()
#             book_match_ratio=difflib.SequenceMatcher(None, search_query_lowercase, book_title_lowercase).ratio()
#             author_match_ratio=difflib.SequenceMatcher(None, search_query_lowercase, book_author_lowercase).ratio()
#             if book_match_ratio >= 0.50 or author_match_ratio >= 0.50:
#                 cart = BookCart()
#                 book_found = True
#                 cart.Book_Title = book.Book_Title
#                 cart.Book_Author = book.Book_Author
#                 cart.Image_URL_M = book.Image_URL_M
#                 cart.Book_Cost = book.Book_Cost
#                 cart.Publisher = book.Publisher
#                 cart.Synopsis = book.Synopsis
#                 cart.ISBN = book.ISBN
#                 context['cart'].append(cart)
#                 print("Found!!--> Book Title:", book.Book_Title, " And Author: ", book.Book_Author)
#         if book_found:
#             return render(request, 'searchresults.html', context )
#         else:
#             return render(request, 'nosearchresults.html', context)
#     return render(request, 'login.html', {})
#
# class Cart(object):
#     model = Books
#
# def searchi(request):
#     return HttpResponse("<h1>In Search Image</h1>")

