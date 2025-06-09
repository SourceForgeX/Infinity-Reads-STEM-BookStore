import datetime
from django.db import models
# from bookstore.models import *
# Create your models here.


class ContactModel(models.Model):
    ContactId=models.BigAutoField(primary_key=True)
    Name=models.TextField(max_length=100)
    Phone=models.IntegerField(null=True)
    Email=models.EmailField(null=True)
    Address=models.TextField(max_length=200)
    def __str__(self):
        return self.Name


class DistrictModel(models.Model):
    DistrictId=models.BigAutoField(primary_key=True)
    District=models.TextField(max_length=40,null=True,unique=True)
    def __str__(self):
        return self.District
    
class LocationModel(models.Model):
     LocationId=models.BigAutoField(primary_key=True)
     District=models.ForeignKey(DistrictModel,on_delete=models.CASCADE)
     Location=models.TextField(max_length=40,null=True)
     def __str__(self):
        return self.Location
    
class CategoryModel(models.Model):
    CategoryId=models.BigAutoField(primary_key=True)
    Category=models.TextField(max_length=50,unique=True)
    Bookimg=models.ImageField(null=True)
    def __str__(self):
        return self.Category
class Sub_CategoryModel(models.Model):
     Sub_Id=models.BigAutoField(primary_key=True) 
     Sub_Category=models.TextField(max_length=50,unique=True)
     Category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
     def __str__(self):
          return self.Sub_Category
     
# Model for Login
class LoginModel(models.Model):
    LoginId=models.BigAutoField(primary_key=True)
    UserName=models.TextField(max_length= 100, null=True)
    Password=models.TextField(max_length=100, null=True)
    Role=models.TextField(max_length=100, null=True)
    Status=models.TextField(max_length=100, null=True)
    # def __str__(self):
    #     return self.UserName

# Model for Registration
class RegisterModel(models.Model):
    RegisterId=models.BigAutoField(primary_key=True)
    RegisterName=models.TextField(max_length= 100, null=True)
    RegisterAddress=models.TextField(max_length= 200, null=True)
    District=models.ForeignKey(DistrictModel, on_delete=models.CASCADE ,null=True)
    Location=models.ForeignKey(LocationModel, on_delete=models.CASCADE ,null=True)
    Email=models.EmailField()
    Phone=models.CharField(max_length= 10, null=True)
    LoginId=models.ForeignKey(LoginModel,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.RegisterName