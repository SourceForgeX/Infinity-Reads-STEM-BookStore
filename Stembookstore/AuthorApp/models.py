from django.db import models

from AdminApp.models import *
# Create your models here.
# class NumberofBooksModel(models.Model):
#         Numid=models.AutoField(primary_key=True)
#         numberofbooks=models.IntegerField(default=None, null=True, blank=True)
#         Bid = models.ManyToManyField("BookRegistrationModel", verbose_name="Books")
class BookRegistrationModel(models.Model):
    Bid=models.AutoField(primary_key=True)
    BookName=models.TextField(max_length=100,null=True,unique=True)
    maincategory=models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    Sub_Category=models.ForeignKey(Sub_CategoryModel,on_delete=models.CASCADE)
    description=models.TextField(max_length=2000,null=True)
    noofpages=models.IntegerField(null=True)
    MRP=models.IntegerField(null=True)
    price=models.IntegerField(null=True)
    year=models.DateField(null=True)
    isbn=models.TextField(null=True)
    language=models.TextField(max_length=20,null=True)
    Author=models.TextField(max_length=20,null=True)
    Publisher=models.TextField(max_length=20,null=True)
    Edition=models.TextField(max_length=20,null=True)
    Bookimg=models.ImageField(null=True)
    username=models.TextField(null=True)
    Status=models.TextField(max_length=100, null=True)
    numberofbooks=models.IntegerField(null=True,default=1)
    total_sales = models.PositiveIntegerField(default=0) 
    BookRegidate=models.DateField(auto_now_add=True, null=True)
    average_rating = models.FloatField(default=0) 
    def __str__(self):
        return self.BookName
    

class Rating(models.Model):
    product = models.ForeignKey(BookRegistrationModel, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # If using Django's User model
    rating = models.IntegerField(default=0)  # Rating value (1 to 5)

    


    