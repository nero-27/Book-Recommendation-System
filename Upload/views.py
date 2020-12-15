from django.http import HttpResponse
import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from Accounts.models import Books
from Accounts.models import Users
from Accounts.models import Ratings
from Accounts.models import Overall_Ratings
from Upload.forms import login_form
from .forms import registration_form
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation
from sklearn.metrics.pairwise import pairwise_distances
from IPython.display import display, clear_output
from contextlib import contextmanager
import ipywidgets as widgets
"""
"""
#uploading Users dataset
@permission_required('admin.can_add_log_entry')
def Users_upload(request):
    template="Users_upload.html"

    #prompt message if CSV fields not in order
    prompt = {
        'order' : 'order of CSV should be Username, Password, Age'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['Users_file']

    #if uploaded file is not CSV
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)     #skip first line of CSV file

    for column in csv.reader(io_string, quotechar="|"):
        _, created = Users.objects.update_or_create(
            Username=column[0],
            Password=column[1],
            Age=column[2]
        )

    context = {}
    return render(request, template, context)

#uploading Books dataset
@permission_required('admin.can_add_log_entry')
def books_upload(request):
    template="books_upload.html"

    #prompt message if CSV fields not in order
    prompt = {
        'order2' : 'order of CSV should be ISBN, Book Title, Book Author, Image-URL-M, Publisher, Synopsis, Book_Cost'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['books_file']

    #if uploaded file is not CSV
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    data_set_books = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set_books)
    next(io_string)     #skip first line of CSV file

    for column in csv.reader(io_string):
        _, created = Books.objects.update_or_create(
            ISBN=column[0],
            Book_Title=column[1],
            Book_Author=column[2],
            Image_URL_M=column[3],
            Publisher=column[4],
            Synopsis=column[5],
            Book_Cost = column[6]
        )

    context = {}
    return render(request, template, context)


#uploading Ratings dataset
@permission_required('admin.can_add_log_entry')
def ratings_upload(request):
    template="ratings_upload.html"

    #prompt message if CSV fields not in order
    prompt = {
        'order3' : 'order of CSV should be Username, ISBN, Book_Rating'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['ratings_file']

    #if uploaded file is not CSV
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    data_set_ratings = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set_ratings)
    next(io_string)     #skip first line of CSV file

    for column in csv.reader(io_string, quotechar="|"):
        _, created = Ratings.objects.update_or_create(
            Username=column[0],
            ISBN=column[1],
            Book_Rating=column[2]
        )

    context = {}
    return render(request, template, context)

#uploading Overall Ratings dataset
@permission_required('admin.can_add_log_entry')
def Overall_Ratings_upload(request):
    template="Overall_Ratings_upload.html"

    #prompt message if CSV fields not in order
    prompt = {
        'order4' : 'order of CSV should be ISBN, Overall Ratings'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['Overall_Ratings_file']

    #if uploaded file is not CSV
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)     #skip first line of CSV file

    for column in csv.reader(io_string, quotechar="|"):
        _, created = Overall_Ratings.objects.update_or_create(
            ISBN=column[0],
            Avg_Rating=column[1]
        )

    context = {}
    return render(request, template, context)

