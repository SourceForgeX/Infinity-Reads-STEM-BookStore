
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from AuthorApp.views import*
from .models import *
from bookstore.models import *
# Create your views here.
# Author index page view
def Authorindex(request):
    Category = CategoryModel.objects.all()
    context = {
   
        "Category": Category,  
    }
    return render(request,'Author/Authorindex.html',context)

def bookregistration(request):
    if request.method == 'POST':
        numbook=request.POST.get("numbooks")
       
        
        bookobj=BookRegistrationModel()
        bookobj.BookName=request.POST.get("txt_bookname")
        category=CategoryModel.objects.get(CategoryId=request.POST.get('ddlCategory'))
        bookobj.maincategory=category    
        subcategory=Sub_CategoryModel.objects.get(Sub_Id=request.POST.get('ddlsubCategory'))
        # print(subcategory)
        bookobj.Sub_Category=subcategory        
        bookobj.description=request.POST.get("txt_bookdescription")        
        bookobj.noofpages=request.POST.get("txt_numberofpages")
        bookobj.MRP=request.POST.get("txt_MRP")
        bookobj.price=request.POST.get("txt_price")
        bookobj.year=request.POST.get("txt_year")
        bookobj.isbn=request.POST.get("txt_ISBN")
        bookobj.language=request.POST.get("txt_Language")
        bookobj.Author=request.POST.get("txt_Author")
        bookobj.Edition=request.POST.get("Edition")
        bookobj.Publisher=request.POST.get("Publisher")
        bookobj.Bookimg=request.FILES.get('book_file')
        bookobj.username = request.session.get('Uname')
        bookobj.Status = "Not Confirmed"
        bookobj.save()
    Category=CategoryModel.objects.all()
    return render(request, 'Author/bookregister.html',{'Category':Category})
# end registration





# fill subcategories view

# def fillSubcategory(request):
#     if request.method == 'POST':
#         did =int(request.POST.get("q"))
#         # category_id = request.POST.get('q')
#         sub=Sub_CategoryModel.objects.filter(Category=did).values(('Sub_Id', 'Sub_Category'))
#         # subcategories = SubCategory.objects.filter(category_id=category_id).values('Sub_Id', 'Sub_Category')
#         return JsonResponse(list(sub), safe=False)
def fillSubcategory(request):
    did =int(request.POST.get("q"))
    print(did)
    sub=Sub_CategoryModel.objects.filter(Category=did).values('Sub_Id', 'Sub_Category')
    for i in sub:
        print(i['Sub_Category'])
    return JsonResponse(list(sub),safe=False)
# end view


# list all his books
def ownbooks(request):
    uname = request.session.get('Uname') 
    # print(uname)
    obj=BookRegistrationModel.objects.filter(username=uname)
    Category = CategoryModel.objects.all()
    context = {
        "dataset":obj,
        "Category": Category,  
    }
    return render(request,'Author/ownbooks.html',context)

 

# Payment datails
def Payment(request):
    
    context = {}  
    uname = request.session.get('Uname') 
    print(uname)
    obj=BookRegistrationModel.objects.filter(username=uname)
 
    context = {
        "dataset":obj,
       
    }
    return render(request,'Author/viewpayment.html',context)



def editBookdetails(request,id):
    
    if request.method=='POST':

        book_instance = get_object_or_404(BookRegistrationModel, Bid=id)
        book_name = request.POST.get("txt_bookname")
        category_id = request.POST.get('ddlCategory')
        description=request.POST.get('txt_description')
        no_of_pages = request.POST.get("txt_numberofpages")
        year_input = request.POST.get("txt_year")
        print(year_input)
        if year_input:
            book_instance.year = year_input
        else:
            book_instance.year = None
        isbn=request.POST.get("TXT_ISBN")
        mrp = request.POST.get("MRP")
        price = request.POST.get("txt_price")
        language = request.POST.get("txt_Language")
        print(language)
        author = request.POST.get("txt_Author")
        edition = request.POST.get("Edition")
        publisher = request.POST.get("Publisher")
        book_image = request.FILES.get('book_file')
        numberofbooks=request.POST.get("book_number")
        print(numberofbooks)
        # Update the book instance with the extracted data
        book_instance.BookName = book_name
        book_instance.noofpages = no_of_pages
        book_instance.MRP = mrp
        book_instance.description=description
        book_instance.price = price
        book_instance.isbn=isbn
        book_instance.language = language
        book_instance.Author = author
        book_instance.Edition = edition
        book_instance.Publisher = publisher
        book_instance.numberofbooks = numberofbooks
        # Handle category selection
        if category_id:
            try:
                category = CategoryModel.objects.get(CategoryId=category_id)
                book_instance.maincategory = category
            except CategoryModel.DoesNotExist:
                # Handle the case where the category does not exist
                pass

         # Handle book image upload
        if book_image:
            book_instance.Bookimg = book_image

        # Save the updated book instance
        book_instance.save()
        # Redirect to a success page or another view
        uname = request.session.get('Uname') 
        obj=BookRegistrationModel.objects.filter(username=uname)
        Category = CategoryModel.objects.all()
        context = {
        "dataset":obj,
        "Category": Category,  
        }

        return render(request,'Author/ownbooks.html',context)
    obj=BookRegistrationModel.objects.get(Bid=id)
    Category = CategoryModel.objects.all()
    context = {
    "data":obj,
    "Category": Category,  # Merge the Category data into the context
    }
    
    return render(request,'Author/editBookdetails.html',context)

def deleteBookdetails(request,id):
    obj=BookRegistrationModel.objects.get(Bid=id)
    obj.delete()
    uname = request.session.get('Uname') 
    obj=BookRegistrationModel.objects.filter(username=uname)
    Category = CategoryModel.objects.all()
    context = {
    "dataset":obj,
    "Category": Category,  # Merge the Category data into the context
    }

    return render(request,'Author/ownbooks.html',context)
def view_district(request):
    District=DistrictModel.objects.all()
    context={
        'District':District,
       
    }
    return render(request,'Author/view_district.html',context)


def get_users_by_author(request,district_id):
    customer_list = []
    uname = request.session.get('Uname') 
    login_id=request.session.get('login_id') 
    # print(uname)
    # print(district_id)
    districtobj=RegisterModel.objects.filter(District=district_id)
    for i in districtobj:
        # print(i.LoginId)
        u=i.LoginId
        
        #
        book=tbl_Booking.objects.filter(customerid=u)
        for bk in book:
            # print(bk.books)
        # for i in book:
            obj=BookRegistrationModel.objects.filter(username=uname)
            if bk.books in obj:
                print(bk.customerid.UserName)
                customer_list.append(bk.customerid.UserName)
        # #         user=i.customerid.LoginId
            
    return render(request,'Author/get_users_by_author.html',{'customer_list': customer_list})

    
def viewlocation(request):
    location=LocationModel.objects.all()
    context={
        'location':location,
       
    }
    return render(request,'Author/view_location.html',context)    

def bylocation(request,location_id):
    customer_list = []
    uname = request.session.get('Uname') 
    login_id=request.session.get('login_id') 
   
    locationobj=RegisterModel.objects.filter(Location=location_id)
    for i in locationobj:
        print(i.LoginId)
        u=i.LoginId
        
        #
        book=tbl_Booking.objects.filter(customerid=u)
        for bk in book:
            # print(bk.books)
        # for i in book:
            obj=BookRegistrationModel.objects.filter(username=uname)
            if bk.books in obj:
                print(bk.customerid.UserName)
                customer_list.append(bk.customerid.UserName)
        # #         user=i.customerid.LoginId
            
    return render(request,'Author/bylocation.html',{'customer_list': customer_list})



    
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Avg
from django.contrib.auth.decorators import login_required


def ajax_rate_product(request, product_id):
    try:
        product = BookRegistrationModel.objects.get(pk=product_id)
        rating_value = int(request.POST.get('rating', 0))

        if 1 <= rating_value <= 5:
            # Update or create a rating
            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating_value}
            )

            # Update product's average rating
            avg_rating = product.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
            product.average_rating = avg_rating
            product.save()

            return JsonResponse({'success': True, 'average_rating': avg_rating})
        else:
            return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5'})

    except BookRegistrationModel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})
