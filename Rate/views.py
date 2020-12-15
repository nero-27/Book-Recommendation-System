from django.shortcuts import render
from django.http import HttpResponse
from Accounts.models import Users, Books, Ratings, Overall_Ratings
import math

class Cart(object):
    model = Books

def rate(request):
    if request.session.has_key('uid'):
        if request.method == 'POST':
            uid =request.session['uid']
            isbn = request.POST['isbn']
            rating_number = request.POST['rating_number']
            if int(rating_number) <=10:
                rated_obj = Ratings.objects.filter(Username = uid);rated=0
                for r in rated_obj:
                    if r.ISBN == isbn:
                        print(r.Book_Rating);rated=1
                        print("User Already Rated So Update USer Rating")
                    else:rated=0
                if rated == 0:
                    print("User Not Rated So Rate")
                    #Add Entry To Ratings DB If Not Rated
                    new_rating = Ratings(Username=uid, ISBN=isbn, Book_Rating=rating_number)
                    new_rating.save()

                # Update Overall_Ratings
                present = Overall_Ratings.objects.filter(ISBN = isbn)
                if present:
                    for p in present:
                        print("Present in OVERALL RATINGS So : Update Rating")
                        previous_rating = p.Avg_Rating
                        print("Previous Rating: ",previous_rating)
                        print("Current Rating: ",rating_number)
                        avg = str(math.ceil(( int(previous_rating) + int(rating_number) ) / 2))
                        print("Updated Rating : ",avg)
                        p.Avg_Rating = avg
                        p.save()
                else:
                    print("Not Present in OVERALL RATINGS So : Add new entry")
                    print("Current Rating: ", rating_number)
                    new_rating = Overall_Ratings(ISBN=isbn, Avg_Rating=rating_number)
                    new_rating.save()

            context = {}
            context['cart'] = []
            cart = Cart()
            cart.Book_Title = request.POST['title']
            cart.Book_Author = request.POST['author']
            cart.Image_URL_M = request.POST['image']
            cart.Book_Cost = request.POST['price']
            cart.Publisher = request.POST['publisher']
            cart.Synopsis = request.POST.get('synopsis')
            cart.ISBN = isbn
            context['cart'].append(cart)
            return render(request, 'detail.html', context)
        return render(request, 'detail.html',{})
    return render(request, 'login.html', {})
