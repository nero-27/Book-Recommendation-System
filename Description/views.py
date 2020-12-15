from django.shortcuts import render, redirect
from django.http import HttpResponse
from Accounts.models import Users, Books, Ratings

class Cart(object):
    model = Books

def description(request):
    if request.session.has_key('uid'):
        if request.method == 'POST':
            context = {}
            context['cart'] = []
            context['post'] = []
            cart = Cart()
            cart.Book_Title = request.POST['title']
            cart.Book_Author = request.POST['author']
            cart.Image_URL_M = request.POST['image']
            cart.Synopsis = request.POST['synopsis']
            cart.Publisher = request.POST['publisher']
            cart.Book_Cost = request.POST['price']
            cart.ISBN = request.POST['isbn']
            context['cart'].append(cart)
            posts = request.session['uid']
            context['post'].append(posts)
            return render(request, 'detail.html', context)
        return render(request, 'detail.html', context)
    return redirect("loginpage")
