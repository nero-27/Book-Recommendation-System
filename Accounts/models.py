from django.db import models

class Books(models.Model):
    ISBN = models.CharField(max_length=100)
    Book_Title = models.CharField(max_length=100)
    Book_Author = models.CharField(max_length=100)
    Book_Cost = models.PositiveIntegerField()
    Publisher = models.CharField(max_length=100)
    Synopsis = models.CharField(max_length=3000)
    Image_URL_M = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.Book_Title} {self.Book_Cost}'

class Users(models.Model):
    # User_ID = models.PositiveIntegerField()
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Age = models.PositiveIntegerField()


    def __str__(self):
        return f'{self.Username}'


class Overall_Ratings(models.Model):
    ISBN = models.CharField(max_length=100)
    Avg_Rating = models.DecimalField(max_digits=5, decimal_places=3)
    books = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.ISBN} {self.Avg_Rating}'

class Ratings(models.Model):
    Username = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=100)
    Book_Rating = models.PositiveIntegerField()
    users = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    books = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True)
    overall = models.ForeignKey(Overall_Ratings, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.Username} {self.Book_Rating}'

