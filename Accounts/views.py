from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from Upload.forms import login_form,registration_form
from Accounts.models import Users, Books, Ratings, Overall_Ratings
from django import forms

#old user recommendations import
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation
from sklearn.metrics.pairwise import pairwise_distances
from IPython.display import display, clear_output
from contextlib import contextmanager
import ipywidgets as widgets
import builtins
from math import sqrt
from sklearn.metrics import mean_squared_error, average_precision_score, r2_score, mean_absolute_error
import seaborn as sns
import matplotlib.pyplot as plt


def signup(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        Username = request.POST["Username"]
        Password = request.POST["Password"]
        Age = request.POST["Age"]
        if form.is_valid():
            print("IN VALID")
            print("NEW USER Saved")
            newusr = Users(Username=Username, Password=Password, Age=Age)
            newusr.save()
            return redirect("loginpage")
        else:
            # print("\n\n\nINVALID : ==>>> ",form.errors.as_data(),"\n\n\n\n")
            return render(request, "signup.html", {'form': form})
    form = registration_form()
    return render(request, "signup.html", {'form': form})

def loginpage(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            # print("In valid")
            username = request.POST['Username']
            uid_session = username
            request.session['uid'] = uid_session
            return redirect("homepage")
        else:
            # print("\n\n\nINVALID : ==>>> ",form.errors.as_data(),"\n\n\n\n")
            return render(request, 'login.html', {'form':form})
    else:
        form = login_form()
        return render(request, 'login.html', {'form':form})
class Cart2:
    model = Books
    model2 = Ratings
def profile(request):
    if request.session.has_key('uid'):
        username = request.session['uid']
        print("\n\n\nIN PROFILE\n\n\n")
        context = {}
        context['books'] = []
        context['user'] = []
        query = Users.objects.get(Username=username)
        books_rated = Ratings.objects.filter(Username = username)
        for b in books_rated:
            book = Books.objects.get(ISBN=b.ISBN)
            print(book.Book_Title)
            cart = Cart2()
            cart.Book_Title = book.Book_Title
            cart.Book_Author = book.Book_Author
            cart.ISBN = book.ISBN
            cart.Book_Rating = b.Book_Rating
            context['books'].append(cart)
        context['user'].append(query)
        return render(request, 'profile.html', context)
    else:
        form = login_form()
        return render(request, 'login.html', {'form':form})

def logout(request):
    try:
        del request.session['uid']
    except:
     pass
    form = login_form()
    return render(request, 'login.html', {'form':form})


class Cart(object):
    model = Books

item_idarray = []
pred_array = []
item_pred_dict = {}
def homepage(request):
    if request.session.has_key('uid'):
        print("in sessions HomePAge")
        uid = request.session['uid']
        rated = Ratings.objects.filter(Username=uid)
        #  RECOMMENDATIONS CORRECT YET AHET KA CHECK KAR COZ USER NE KAMI RATE KELA TARI SAME RECMMENDATIONS YET AHET
        # !!!!!!!!!!!!!!!!!!!!!!!!! OLD USER RATINGS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if rated:
            context = {}
            context['cart'] = []
            context['post'] = []
            # print("\n\n\nOld USer\n\n\n")

            df_all_books_isbn = pd.DataFrame(list(Books.objects.values('ISBN')))
            df_all_ratings = pd.DataFrame(list(Ratings.objects.values('Username', 'ISBN', 'Book_Rating')))
            # old user homepage recommendation code

            # generating ratings matrix for explicit ratings
            # considering users who rated 100 books and books which have been rate 100 times.
            counts1 = df_all_ratings['Username'].value_counts()
            ratings_explicit = df_all_ratings[df_all_ratings['Username'].isin(counts1[counts1 >= 1].index)]
            counts = ratings_explicit['Book_Rating'].value_counts()
            ratings_explicit = ratings_explicit[ratings_explicit['Book_Rating'].isin(counts[counts >= 1].index)]
            # print("RATINGS EXP", ratings_explicit)

            ratings_matrix = ratings_explicit.pivot_table(index='Username', columns='ISBN', values='Book_Rating')
            # print(ratings_matrix)
            usernm = ratings_matrix.index
            ISBN = ratings_matrix.columns

            ratings_matrix.fillna(0, inplace=True)
            ratings_matrix = ratings_matrix.astype(np.int32)
            # print("printing Ratings matrix head after replacing NaN with 0")
            print(ratings_matrix.loc[[uid]])
            current_user_row_matrix = ratings_matrix.loc[[uid]]
            # print(ratings_matrix.columns)
            matrix_cols = pd.DataFrame(ratings_matrix.columns).index
            # print(matrix_cols.index)
            # Item-based CF
            # print("konuecwisnabuwnfmc")
            print(ratings_matrix)
            # setting global variables
            global metric, k
            k = 10
            metric = 'cosine'

            def findksimilaritems(item_id, ratings, metric=metric, k=k):
                similarities = []
                indices = []
                ratings = ratings.T
                loc = ratings.index.get_loc(item_id)
                model_knn = NearestNeighbors(metric=metric, algorithm="brute")
                model_knn.fit(ratings)
                distances, indices = model_knn.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors=k + 1)
                similarities = 1 - distances.flatten()
                # print('findksimilar function executed')
                return similarities, indices

            # This function predicts the rating for specified user-item combination based on the item-based approach
            def predict_itembased(user_id, item_id, ratings, metric=metric, k=k):
                prediction = wtd_sum = 0
                user_loc = ratings.index.get_loc(user_id)
                item_loc = ratings.columns.get_loc(item_id)

                # similar users based on correlation coefficients
                similarities, indices = findksimilaritems(item_id, ratings)
                sum_wt = np.sum(similarities) - 1
                product = 1
                for i in range(0, len(indices.flatten())):
                    if indices.flatten()[i] == item_loc:
                        continue
                    else:
                        product = ratings.iloc[user_loc, indices.flatten()[i]] * (similarities[i])
                        wtd_sum = wtd_sum + product
                    prediction = round(wtd_sum / sum_wt)

                # below code is to avoid negative predictions which might arise in case of very sparse datasets when using correlation metric

                if prediction <= 0:
                    prediction = 1
                elif prediction > 10:
                    prediction = 10
                item_idarray.append(item_id)
                pred_array.append(prediction)
                return prediction

            # prediction=predict_itembased(2276 ,'000649840X', ratings_matrix)

            def recommendItem(user_id, ratings, metric=metric):
                prediction = []
                for i in range(ratings.shape[1]):
                    if ratings[str(ratings.columns[i])][user_id] != 0:  # not rated already
                        prediction.append(predict_itembased(user_id, str(ratings.columns[i]), ratings, metric))
                    else:
                        prediction.append(-1)
                prediction = pd.Series(prediction)
                prediction = prediction.sort_values(ascending=False)
                recommended = prediction[:21]
                # a = Books.objects.get(Book_Author = "");i=0
                # a.Book_Author = "Charles Dickens"
                # a.save()
                # for book in a:
                #     print(i,"\t",book.Book_Author,"\t",book.Book_Title,"\t",book.Synopsis,"\n\n");i=i+1
                # a.delete()
                for i in range(len(recommended)):
                    cart = Cart()
                    book = Books.objects.get(ISBN=df_all_books_isbn.ISBN[recommended.index[i]])
                    cart.Book_Title = book.Book_Title
                    cart.Book_Author = book.Book_Author
                    cart.Image_URL_M = book.Image_URL_M
                    cart.Synopsis = book.Synopsis
                    cart.Book_Cost = book.Book_Cost
                    cart.Publisher = book.Publisher
                    cart.ISBN = book.ISBN
                    context['cart'].append(cart)

                    print(i, "\t", book.Book_Title, "\t", book.Book_Author)


                # ------------------------------ RECOMMENDER SYSTEM EVALUATION (RMSE) ---------------------------------

                print('-----------------THIS IS PREDICTION-----------------')
                print(recommended)
                recommended_indices = recommended.index
                actual_ratings_isbn = []            # isbn of books having indices common with predicted ratings array
                for i in matrix_cols:
                    for j in recommended_indices:
                        if i==j:
                            actual_ratings_isbn.append(ratings_matrix.columns[i])

                # print(actual_ratings_isbn)

                actual_ratings = []       # isbn of books common in ratings matrix and predicted ratings array
                for i in ratings_matrix.columns:
                    for j in actual_ratings_isbn:
                        if i==j:
                            # recommended_isbn.append(i)
                            actual_ratings.append(current_user_row_matrix[i])

                # converting actual ratings and recommended(predicted ratings) into pandas series
                df_actual_ratings = pd.Series(actual_ratings)
                df_recommended = pd.Series(recommended)
                # print(df_actual_ratings)

                # Calculating and printing RMSE value
                print("RMSE VALUE")
                print(sqrt(mean_squared_error(df_actual_ratings, df_recommended)))

                # Get number of ratings and rmse value for 5 users
                user1_ratings_count = ratings_matrix.loc['aa'].value_counts()
                user2_ratings_count = ratings_matrix.loc['jaya'].value_counts()
                user3_ratings_count = ratings_matrix.loc['richa'].value_counts()
                user4_ratings_count = ratings_matrix.loc['abcd'].value_counts()
                user5_ratings_count = ratings_matrix.loc['B5Ic3K'].value_counts()

                # appending no of ratings values in a dataframe
                no_of_ratings = []
                no_of_ratings.extend(
                    [user1_ratings_count[1:].sum(), user5_ratings_count[1:].sum(), user2_ratings_count[1:].sum(),
                     user4_ratings_count[1:].sum(), user3_ratings_count[1:].sum()]
                )
                print(no_of_ratings)

                rmse_of_users = [3.484660262185848, 3.7032803990902057, 4.281744192888376, 5.282495802626056,
                                 5.661061653755332]

                plt.scatter(no_of_ratings, rmse_of_users, color='red')
                plt.plot(no_of_ratings, rmse_of_users)
                plt.xlabel('no of ratings')
                plt.ylabel('RMSE value')
                plt.show()

            recommendItem(uid, ratings_matrix)

            query = Users.objects.get(Username=uid)
            username = query.Username
            context['post'].append(username)
            return render(request, 'home_af_lg.html', context)


        # !!!!!!!!!!!!!!!!!!!! END OLD USER RATINGS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            # $$$$$$$$$$$$$$$$ NEW USER RATINGS $$$$$$$$$$$$$$$$$$$
            context = {}
            context['cart'] = []
            context['post'] = []
            count=0
            top_ratings = Overall_Ratings.objects.filter(Avg_Rating__gte=10)[:22]
            for top_rating in top_ratings:
                count = count + 1
                top_books = Books.objects.filter(ISBN=top_rating.ISBN)
                for book in top_books:
                    cart = Cart()
                    cart.Book_Title = book.Book_Title
                    cart.Book_Author = book.Book_Author
                    cart.Image_URL_M = book.Image_URL_M
                    cart.Synopsis = book.Synopsis
                    cart.Book_Cost = book.Book_Cost
                    cart.Publisher = book.Publisher
                    cart.ISBN = book.ISBN
                    context['cart'].append(cart)
                    print(count, " ", book)

            query = Users.objects.get(Username=uid)
            username = query.Username
            context['post'].append(username)
            return render(request, 'home_af_lg.html', context)
            # $$$$$$$$$$$$$$$$ END NEW USER RATINGS $$$$$$$$$$$$$$$$$$$

    return render(request, 'home.html', {})