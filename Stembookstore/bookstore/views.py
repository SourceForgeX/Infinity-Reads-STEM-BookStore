from pyexpat.errors import messages
import random
from django.db.models import ExpressionWrapper, F, DecimalField
from django.forms import IntegerField
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from AdminApp.models import*
from AuthorApp.models import*
from django.db.models import Q
from email.message import EmailMessage
import smtplib
from django.contrib.auth.hashers import make_password
# Create your views here.

def index(request):
    
    top_books = BookRegistrationModel.objects.order_by('-total_sales')[:5]  # Show top 5 on homepage
   
    recent_books = BookRegistrationModel.objects.order_by('-BookRegidate')[:10]  # Fetch the 10 most recent books
    
    Category = CategoryModel.objects.all()
    context = {
        # "dataset": data,
        "Category": Category,  # Merge the Category data into the context
        'top_books': top_books,
        'recent_books': recent_books
    }
    
                               
    return render(request, 'Customer/index.html',context)


def home(request):
    return render(request,'Author/home.html')

def login(request):
    if request.method=='POST':
        
        U_name=request.POST.get("txt_username")
        Password=request.POST.get("txt_password")
        if LoginModel.objects.filter(UserName=U_name,Password=Password).exists():
            Category = CategoryModel.objects.all()
            context = {
   
                "Category": Category,  
                }
            loginobj=LoginModel.objects.get(UserName=U_name,Password=Password)
            request.session['Uname']=loginobj.UserName
            request.session['login_id']=loginobj.LoginId
            role=loginobj.Role
            Status=loginobj.Status
            if role=='Admin':
                return render(request,'Admin/adminindex.html')
            elif role=='Author':
                if Status=='Not Confirmed':
                    return render(request,'login.html',{"ERROR":"Please wait for Confirmation"})
                else:
                   
                    return render(request,'Author/Authorindex.html',context)
            else:
                 return redirect('/index') 
                #  return render(request,'Customer/index.html',context)
        else:
         return render(request, 'login.html', {'ERROR': 'Invalid Credentials'})
    else:
       
        return render(request,'login.html')

def registration(request):
    print("---")
    if request.method=='POST':
        Name=request.POST.get("name")
        Address=request.POST.get("address")
        Email=request.POST.get("email")
        PhoneNumber =request.POST.get("phone")
        District=request.POST.get("ddldistrict")
        Location=request.POST.get("")

        UserName=request.POST.get("UserName")
        Password=request.POST.get("password")
        ConfirmPassword=request.POST.get("confirmpassword")
        Role=request.POST.get("Role")
        loginobj=LoginModel()
        if LoginModel.objects.filter(UserName=request.POST.get("UserName")).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='registration';</script>")
        else:
            if Password==ConfirmPassword:
                loginobj.UserName=UserName
                loginobj.Password=Password
                loginobj.Role=Role
                if loginobj.Role=='Author':
                    loginobj.Status="Not Confirmed"
                else:
                    loginobj.Status="Confirmed"
                loginobj.save()
                Registerobj=RegisterModel()
                Registerobj.RegisterName=Name
                Registerobj.RegisterAddress=Address
                Registerobj.Email=Email
                Registerobj.Phone=PhoneNumber
                Registerobj.LoginId=loginobj
                Registerobj.save()

               
                
                email = request.POST.get('email')  # to address
                print(email)
                msg = EmailMessage()
                msg.set_content('Body')
                msg['Subject'] = "Registration Completed"
                msg['From'] = 'projectdjango12345@gmail.com'
                msg['To'] = email  # Get email from form input

                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login('projectdjango12345@gmail.com', 'fzxi ooyw owyk vakx')  # Use App Password
                        smtp.send_message(msg)

                        return HttpResponse("<script>alert('Successfully Registered');window.location='login';</script>")
                except Exception as e:
                    return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='registration';</script>")

    District = DistrictModel.objects.all()
    return render(request,'registration.html',{'District':District})

def filllocation(request):
    did =int(request.POST.get("q"))
  
    sub=LocationModel.objects.filter(District=did).values()
   

    return JsonResponse(list(sub),safe=False)


def listofbooksview(request):
    Category = CategoryModel.objects.all()
    dataset=BookRegistrationModel.objects.filter(Status="Confirmed")
    
    context = {
        "dataset": dataset,
        "Category": Category,  # Merge the Category data into the context
    }
    return render(request, 'Customer/listofbooks.html', context)
# View ends

def Bookdetails(request, id):
    
    Category = CategoryModel.objects.all()
    bookobj = get_object_or_404(BookRegistrationModel, Bid=id)  # Fetch book safely
   
    feedback = FeedBackModel.objects.filter(book=bookobj.BookName)  # Get all feedbacks
    print(bookobj.BookName)
    
    for f in feedback:
        print(f.book)
    
    request.session['bid'] = bookobj.Bid

    context = {
        "data": bookobj,
        "Category": Category,
        "dataset": feedback, 
    }

    return render(request, 'Customer/Bookdetails.html', context)


def secondhandbook(request):
    if request.method == 'POST':
        bookobj=secondhandBookModel()
        bookobj.BookName=request.POST.get("txt_bookname")
        category=CategoryModel.objects.get(CategoryId=request.POST.get('ddlCategory'))
        bookobj.maincategory=category           
        bookobj.noofpages=request.POST.get("txt_numberofpages")
        bookobj.MRP=request.POST.get("MRP")
        bookobj.price=request.POST.get("txt_price")
        bookobj.year=request.POST.get("txt_year")
        bookobj.language=request.POST.get("ddlLanguage")
        bookobj.Author=request.POST.get("txt_Author")
        bookobj.Edition=request.POST.get("Edition")
        bookobj.Publisher=request.POST.get("Publisher")
        bookobj.Bookimg=request.FILES.get('book_file')
        bookobj.username = request.session.get('Uname')
        bookobj.Status = "Not Sale"
        bookobj.save()
    Category=CategoryModel.objects.all()
    return render(request, 'Customer/secondhandbook.html',{'Category':Category})



def search(request):
    if request.method=="POST":
        search=request.POST.get("txt_search")
        context={}
        context = {
        "dataset": BookRegistrationModel.objects.filter(Q(BookName=search) | Q(Author=search) )
         }

    return render(request,"Customer/search.html",context)


def contact(request):
    context={}
    context["dataset"]=ContactModel.objects.all()
    return render(request,"Customer/contact.html",context)  

def feedback(request):
    if request.method == 'POST':
        Name=request.session.get('Uname')
        Bookname=request.POST.get("BookName")
        Message=request.POST.get("feedback")
        rating=request.POST.get("rating")
        feedbackobj=FeedBackModel()
        feedbackobj.FName=Name
        feedbackobj.book=Bookname
        feedbackobj.Message=Message
        feedbackobj.rating=rating
        feedbackobj.save()
        # return render(request,"Author/ajax_rate_product.html",Bookname)

    user = request.session.get('login_id') 
    books = tbl_Booking.objects.filter(customerid=user).values_list('books', flat=True).distinct()
    book_objs = BookRegistrationModel.objects.filter(Bid__in=books)  # Replace BookModel with your actual model name
    
    context = {
        'books': book_objs
    }

    return render(request,"Customer/feedback.html",context)  

def newpassword(request):
    login_id= request.session.get('login_id')
    user = RegisterModel.objects.get(LoginId=LoginModel.objects.get(LoginId=login_id))
    email=user.Email
    # print(user.Email)
    msg = EmailMessage()
    msg.set_content('Body')
    msg['Subject'] = "Your password is v12"
    msg['From'] = 'projectdjango12345@gmail.com'
    msg['To'] = email  # Get email from form input

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('projectdjango12345@gmail.com', 'fzxi ooyw owyk vakx')  # Use App Password
            smtp.send_message(msg)

            return HttpResponse("<script>alert('code send to the mail');window.location='changepassword';</script>")
    except Exception as e:
         return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='login';</script>")
    
from django.shortcuts import render

def changepassword(request):
    if request.method == "POST":
        txtmail = request.POST.get("txt_email")
        # print(txtmail)
        if txtmail == 'v12':
            return render(request, 'Customer/changepasswordset.html')
        else:
            return render(request, 'login.html')
    
    # Ensure GET request also returns a response
    return render(request, 'Customer/changepassword.html')
def changepasswordset(request):
    if request.method == "POST":
        password = request.POST.get("txt_password")
        confirmpassword = request.POST.get("txt_confirm_password")
        username = request.POST.get("txt_username")
        user=LoginModel.objects.filter(UserName=username)
        if user.exists():
            if password == confirmpassword:
                u = user.first()
                u.Password = make_password(password)
                u.save()
                return HttpResponse("<script>alert('Password changed successfully');window.location='login';</script>")
            else:
                return HttpResponse("<script>alert('code send to the mail');window.location='changepassword';</script>")
        else:
             return HttpResponse("<script>alert('User not excist');window.location='login';</script>")
        # if txtmail == 'v12':
        #     return render(request, 'Customer/changepasswordset.html')
        # else:
        #     return render(request, 'Customer/login.html')
    
    # Ensure GET request also returns a response
    return render(request, 'Customer/changepasswordset.html')


    

# to display all the books
def listofsecondbooksview(request):
    Category = CategoryModel.objects.all()
    # dataset = secondhandBookModel.objects.filter(Status!='paid')
    dataset= secondhandBookModel.objects.exclude(Status='Sold')
    if not dataset:
        # Handle the case when no books are found for the given category id
        context = {
            "message": "No books found .",
            "Category": Category,
        }
    else:
        context = {
            "dataset": dataset,
            "Category": Category,  # Merge the Category data into the context
        }
    return render(request, 'Customer/listsecondbooks.html', context)

def secondBookdetails(request,id):
    Category = CategoryModel.objects.all()
    context = {
        "data": secondhandBookModel.objects.get(Secondid=id),
        "Category": Category,  # Merge the Category data into the context
    }
    return render(request,'Customer/secondBookdetails.html',context)


def CategoryBookdetails(request,id):
    data=BookRegistrationModel.objects.filter(maincategory=id)
    Category = CategoryModel.objects.all()
    if not data:
        # Handle the case when no books are found for the given category id
        context = {
            "message": "No books found for this category.",
            "Category": Category,
        }
    else:
        context = {
            "dataset": data,
            "Category": Category,  # Merge the Category data into the context
        }
    return render(request,"Customer/maincategory.html",context)



def aboutus(request):
    return render(request,'Customer/aboutus.html')

def ownbooksview(request):
    uname = request.session.get('Uname') 
    print(uname)
    obj=secondhandBookModel.objects.filter(username=uname)
    Category = CategoryModel.objects.all()
    context = {
            "dataset":obj,
         "Category": Category,  # Merge the Category data into the context
         
        }
   
    return render(request,'Customer/ownbooksview.html',context)

def deletesecondBookdetails(request,id):
    obj=secondhandBookModel.objects.get(Secondid=id)
    obj.delete()
    uname = request.session.get('Uname') 
    obj=secondhandBookModel.objects.filter(username=uname)
    Category = CategoryModel.objects.all()
    context = {
        "dataset":obj,
        "Category": Category,  # Merge the Category data into the context
    }
   
    return render(request,'Customer/ownbooksview.html',context)

def editsecondBookdetails(request,id):
    obj=secondhandBookModel.objects.get(Secondid=id)
    Category = CategoryModel.objects.all()
    context = {
        "data":obj,
        "Category": Category,  # Merge the Category data into the context
    }
    if request.method=='POST':

        book_instance = get_object_or_404(secondhandBookModel, Secondid=id)
        book_name = request.POST.get("txt_bookname")
        category_id = request.POST.get('ddlCategory')
        no_of_pages = request.POST.get("txt_numberofpages")
        year_input = request.POST.get("txt_year")
        if year_input:
            book_instance.year = year_input
        else:
            book_instance.year = None
        
        mrp = request.POST.get("MRP")
        price = request.POST.get("txt_price")
        language = request.POST.get("ddlLanguage")
        author = request.POST.get("txt_Author")
        edition = request.POST.get("Edition")
        publisher = request.POST.get("Publisher")
        book_image = request.FILES.get('book_file')

        book_instance.BookName = book_name
        book_instance.noofpages = no_of_pages
        book_instance.MRP = mrp
        book_instance.price = price
        book_instance.language = language
        book_instance.Author = author
        book_instance.Edition = edition
        book_instance.Publisher = publisher

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
        return render(request,'Customer/index.html',context)

    obj=secondhandBookModel.objects.get(Secondid=id)
    Category = CategoryModel.objects.all()
    context = {
        "data":obj,
        "Category": Category,  # Merge the Category data into the context
    }
    return render(request,'Customer/editsecondBookdetails.html',context)

def buynow(request,id):
    book=secondhandBookModel.objects.get(Secondid=id)
    Loginid=request.session.get('login_id')
    print(book)
    print(Loginid)
    buynow=BuyNowModel()
    buynow.bookname=book
    buynow.custerid=LoginModel.objects.get(LoginId=Loginid)
    buynow.save()
    book.Status='Solds'
    book.save()
    last_inserted = BuyNowModel.objects.latest('buynowid')
    
    return render(request,'Customer/buynow.html',{'lastinsert':last_inserted}) 





def add_to_cart(request, product_id):

    request.session['cart']="cart"
    if request.method=='POST':
        
        if request.POST.get('cart')=="Add to Cart" :
            bid=BookRegistrationModel.objects.get(Bid=product_id)
           
            qty = int(request.POST.get("qty", 1)) 
            print(qty)
            if int(bid.numberofbooks) <= 0:
                
                return HttpResponse("<script>alert('Stock exceeded.');window.location='/listofbooksview';</script>")
            else:
                cart = CartItemModel.objects.filter(Bid=bid).first()
                
                if cart:
               
                    Qty = cart.quantity or 0  
                    Qty += qty
                    cart.quantity=Qty
                    cart.save()
                else:
                    cart_obj=CartItemModel()
                    cart_obj.Bid=bid
                    cart_obj.custerid=LoginModel.objects.get(LoginId=request.session.get('login_id'))
                    cart_obj.quantity=1
                    cart_obj.status="cart"
                    # bid.numberofbooks=bid.numberofbooks-1
                    # print(bid.numberofbooks)
                    bid.save()
                    cart_obj.save()
                print("hai")
                bid.numberofbooks -= qty
                print(bid.numberofbooks)
                # bid.save(update_fields=['numberofbooks'])
                bid.total_sales += qty
                print(bid.total_sales)
                print("---------")
                bid.save()
    return redirect('view_cart')
        
        
 
    
        
    
def view_cart(request):
    sub_totals = [] 
    sub_total=0
    Quantity=0
    cart_items=CartItemModel.objects.filter(custerid=request.session.get('login_id'),status='cart')
    # cart_total = cart_items.get_total_price() if cart_items else 0 
    # print(cart_total)

    sub_totals = [ item.quantity * item.Bid.price  for item in cart_items]
    Quantity=[Quantity+item.quantity  for item in cart_items]
    Qty=sum(Quantity)
    sub_total = sum(sub_totals)
    grandtotal = sub_total * 1.1  # Adding 10% tax
    context = {
         'sub_totals': sub_totals,
        'cart_items': cart_items,
        'sub_total': sub_total,
        'grandtotal': grandtotal,
        'Quantity':Qty,
     
    }
      
    return render(request, 'Customer/cart.html',context)
        
        
def update_cart(request, item_id):
   
    cart_item = get_object_or_404(CartItemModel,CartId=item_id)
    bid=BookRegistrationModel.objects.get(Bid=cart_item.Bid.Bid)
   
    print(bid.numberofbooks)
    if request.method == "POST":
        action = request.POST.get("action")
        current_quantity = cart_item.quantity
       
           
        if action == "increase":
            cart_item.quantity += 1
            if int(bid.numberofbooks) <= 0:
                
                return HttpResponse("<script>alert('Stock exceeded.');window.location='/listofbooksview';</script>")
            bid.numberofbooks=bid.numberofbooks-1
        elif action == "decrease" and current_quantity > 1:
             
            cart_item.quantity -= 1
            bid.numberofbooks=bid.numberofbooks+1
            
        cart_item.save()
        bid.save()
            
    return redirect('view_cart')

def makepayment(request):
    if request.method == 'POST':
        grandtotal = request.POST.get('gtotal')
        
        booking = tbl_Booking_master.objects.create(
            customerid=LoginModel.objects.get(LoginId=request.session.get('login_id')),
            Total=grandtotal,
            Billnumber=tbl_Booking_master.objects.latest('Billnumber').Billnumber + 1,
            status="booking"
        )
        
        cart_items = CartItemModel.objects.filter(
            custerid=request.session.get('login_id'), status='cart'
        )
        
        for item in cart_items:
            tbl_Booking.objects.create(
                books=item.Bid,
                qty=item.quantity,
                Master=booking,
                status="booking",
                customerid=LoginModel.objects.get(LoginId=request.session.get('login_id')),
            )
        
        context = {
            'booking': booking,  # Use 'booking' instead of 'bookingObj'
            'grandtotal': grandtotal,
        }
        
        return render(request, 'customer/payment.html', context)
    
    return render(request, 'customer/payment.html')




def placeorder(request,id):
    
    if request.method=='POST':
        customerid=RegisterModel.objects.get(LoginId=request.session.get('login_id'))
        print(customerid.Email)
        paymentObj=PaymentModels()
        total=0.0
        gtotal=float(request.POST.get('gtotal'))
        print(gtotal)
        total=gtotal*0.4
        print(total)
        paymentObj.CardNo=request.POST.get('cardno')
        paymentObj.CardName=request.POST.get('cardname')
        paymentObj.CVV=request.POST.get('cvv')
        paymentObj.Deliveryaddress=request.POST.get('Deliveryaddress')
        paymentObj.status="paid"
        paymentObj.save()
        pid=paymentObj.PaymentId
        print(pid)
        cart_obj=CartItemModel.objects.filter(custerid=request.session.get('login_id'))
     
        
        cart_obj.delete()
        
        books = get_object_or_404(tbl_Booking_master,masterid=id)
        book=tbl_Booking.objects.filter(Master=books.masterid , status='booking')
        for i in book:
            print("hai")
            uname = i.books.username
            print(uname)
    
            email_obj = RegisterModel.objects.filter(LoginId__UserName=uname).first()
            if email_obj:
                email=email_obj.Email
            else:
                print("Email not found for username:", uname)

        mail="mca2325_alvinantony@santhigiricollege.com"
        msg = EmailMessage()
        msg.set_content('Body')
        msg['Subject'] = "Dear Author, INR {:.2f} is credited to your account".format(total)

        msg['From'] = 'projectdjango12345@gmail.com'
        msg['To'] = "mca2325_alvinantony@santhigiricollege.com"  # Get email from form input

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('projectdjango12345@gmail.com', 'fzxi ooyw owyk vakx')  # Use App Password
                smtp.send_message(msg)

                return HttpResponse("<script>alert('Successfully Ordered');window.location='/listofbooksview';</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='registration';</script>")



        return redirect('paymentdetails',pid)

    return render(request, 'Customer/index.html')

def paymentdetails(request,pid):  
   
    payment = get_object_or_404(PaymentModels, PaymentId=pid)
    # return HttpResponse("<script>alert('Payment Successfully done.');window.location='/paymentdetails';</script>")
    print(payment.CardName)  # Debugging print
    return render(request, 'Customer/paymentdetails.html', {'payment': payment})  
 
def remove_from_cart(request, cart_id):
    cart_items=CartItemModel.objects.get(CartId=cart_id)
    cart_items.delete()
    return redirect('view_cart')

def clear_cart(request):

    cart_obj=CartItemModel.objects.filter(custerid=request.session.get('login_id'))
   
    cart_obj.delete()
    # request.session.pop('cart', None)
    # messages.success(request, "Your cart has been cleared.")
    return redirect('view_cart')




# bestsellers
def bestsellers(request):
    print("hai")
    top_books = BookRegistrationModel.objects.order_by('-total_sales')[:10]  # Top 10 bestsellers
    Category = CategoryModel.objects.all()
    context = {
        # "dataset": data,
        "Category": Category,  # Merge the Category data into the context
        'top_books': top_books,
    }
    return render(request, 'Customer/bestsellers.html', context)

# new arrivals
def new_arrivals(request):
    recent_books = BookRegistrationModel.objects.order_by('-BookRegidate')[:10]  # Fetch the 10 most recent books
    return render(request, 'new_arrivals.html', {'recent_books': recent_books})