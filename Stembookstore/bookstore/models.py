from django.db import models
from AdminApp.models import *
from AuthorApp.models import *

# Create your models here.


    
    # category of Books
 

class secondhandBookModel(models.Model):
    Secondid=models.AutoField(primary_key=True)
    BookName=models.TextField(max_length=100,null=True,unique=True)
    maincategory=models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    noofpages=models.IntegerField(null=True)
    MRP=models.IntegerField(null=True)
    price=models.IntegerField(null=True)
    year = models.DateField(default=None, null=True, blank=True)
    language=models.TextField(max_length=20,null=True)
    Author=models.TextField(max_length=20,null=True)
    Publisher=models.TextField(max_length=20,null=True)
    Edition=models.TextField(max_length=20,null=True)
    Bookimg=models.ImageField(null=True)
    username=models.TextField(null=True)
    Status=models.TextField(max_length=100, null=True)
    def __str__(self):
        return self.BookName
  


class BuyNowModel(models.Model):
    buynowid = models.AutoField(primary_key=True)
    bookname = models.ForeignKey(secondhandBookModel, on_delete=models.CASCADE)
    custerid = models.ForeignKey(LoginModel, on_delete=models.CASCADE)
class CartItemModel(models.Model):
    CartId=models.AutoField(primary_key=True)
    Bid=models.ForeignKey(BookRegistrationModel,on_delete=models.CASCADE)
    custerid=models.ForeignKey(LoginModel,on_delete=models.CASCADE)
    quantity=models.BigIntegerField(default=1)
    status=models.CharField(max_length=30)

    def get_total_price(self):
        return self.quantity * self.Bid.price  
    


class tbl_Booking_master(models.Model):
 
    masterid = models.AutoField(primary_key=True)  # Correct way to define AutoField
    Bookingdate = models.DateField(auto_now_add=True)
    Total = models.FloatField(default=0.0)
    # books = models.ForeignKey(BookRegistrationModel, on_delete=models.CASCADE)
    customerid = models.ForeignKey(LoginModel, on_delete=models.CASCADE, null=True)
    Billnumber = models.IntegerField(default=100)
    status = models.CharField(max_length=100,null=True,default='not booking')

class tbl_Booking(models.Model):
    BookingId=models.AutoField(primary_key=True)
    Master=models.ForeignKey(tbl_Booking_master,on_delete=models.CASCADE)
    books=models.ForeignKey(BookRegistrationModel,on_delete=models.CASCADE)
    # price=models.IntegerField(default=0)
    qty=models.IntegerField(default=0)
    customerid=models.ForeignKey(LoginModel,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100 ,null=True,default='not booking')
    def __str__(self):
        return f"Booking {self.BookingId} - {self.status}"
    

class PaymentModels(models.Model):
    PaymentId = models.AutoField(primary_key=True)
    CardNo = models.BigIntegerField()
    CardName=models.CharField(max_length=40)
    CVV=models.IntegerField()
    Deliveryaddress	=models.TextField(max_length=100,null=True)
    status=models.CharField(max_length=100)

class FeedBackModel(models.Model):
    FeedBackId=models.BigAutoField(primary_key=True)
    FName=models.TextField(max_length=100, null=True)
    # user=models.ForeignKey(tbl_Booking,on_delete=models.CASCADE)
    book=models.TextField(max_length=500,null=True,default=None)
    Message=models.TextField(max_length=200,null=True)
    FeedBackdate=models.DateField(default=datetime.date.today)
    rating=models.IntegerField(default=0,null=True)
    class Meta:
        ordering = ['-FeedBackdate']
    def __str__(self):
        return self.FName if self.FName else "Unnamed Feedback"
    
    