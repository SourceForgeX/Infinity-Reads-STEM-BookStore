from email.message import EmailMessage
from pyexpat.errors import messages
import smtplib
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from AdminApp.models import *
from AuthorApp.models import *
from bookstore.models import *
from django.db.models import Sum
import xlwt

from django.views.generic import View

# Create your views here.
def district(request):
    if request.method=='POST':
        Districtobj=DistrictModel()
        Districtobj.District=request.POST.get("txt_district")
        Districtobj.save()
    return render(request,"Admin/district.html")

def Location(request):
    if request.method=='POST':
        locationobj=LocationModel()
        locationobj.Location=request.POST.get("txt_location")
        District=DistrictModel.objects.get(DistrictId=request.POST.get('district'))
        locationobj.District=District
        locationobj.save()
    District=DistrictModel.objects.all()
    return render(request,"Admin/location.html",{'District':District})

def categoryView(request):
    if request.method=='POST':
        categoryobj=CategoryModel()
        categoryobj.Category=request.POST.get("txt_Category")
        print("txt_Category")
        categoryobj.save()
    return render(request,"Admin/Category.html")

def subCategoryView(request):
    if request.method=='POST':
        subCategoryobj=Sub_CategoryModel()
        subCategoryobj.Sub_Category=request.POST.get("txt_subCategory")
        Category=CategoryModel.objects.get(CategoryId=request.POST.get('category'))
        subCategoryobj.Category=Category
        subCategoryobj.save()
    Category=CategoryModel.objects.all()
    return render(request,"Admin/sub_category.html",{'Category':Category})

def adminindex(request):
     return render(request,"Admin/adminindex.html")

def feedbackview(request):
    feedback=FeedBackModel.objects.all()

    return render(request,'Admin/feedbackview.html',{'feedback':feedback})

def deletefeedback(request,id):
    feedback=FeedBackModel.objects.get(FeedBackId=id)
    feedback.delete()
    return redirect('/feedbackview')   

def statusbook(request):
    books=BookRegistrationModel.objects.all()
    return render(request,'Admin/statusbook.html',{'books':books})

def changestatusbook(request,id):
    books=BookRegistrationModel.objects.get(Bid=id)
    books.Status="Confirmed"
    books.save()
    username=books.username
    print(username)
    user=RegisterModel.objects.filter(RegisterName=username)
    for u in user:
        print("hai")
        print(u.Email)

        email = u.Email  # to address
        # email="alvin@gmail.com"
        msg = EmailMessage()
        msg.set_content('Body')
        msg['Subject'] = "Registration Completed"
        msg['From'] = 'projectdjango12345@gmail.com'
        msg['To'] = email  # Get email from form input
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('projectdjango12345@gmail.com', 'fzxi ooyw owyk vakx')  # Use App Password
                smtp.send_message(msg)
                # books=BookRegistrationModel.objects.all()
                # return HttpResponse("<script>alert('Successfully Registered');window.location='adminindex';</script>")
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='registration';</script>")


    books=BookRegistrationModel.objects.all()
    return render(request,'Admin/statusbook.html',{'books':books})

def statususer(request):
    users=LoginModel.objects.all()
    return render(request,'Admin/statususer.html',{'users':users})
def changestatususer(request,id):
    users=LoginModel.objects.get(LoginId=id)
    users.Status="Confirmed"
    users.save()
    # username=books.username
    # print(username)
    user=RegisterModel.objects.get(LoginId=users.LoginId)
    # for u in user:
        # print("hai")
    print(user.Email)

    email = user.Email  # to address
    # email="alvin@gmail.com"
    msg = EmailMessage()
    msg.set_content('Body')
    msg['Subject'] = "Registration Completed"
    msg['From'] = 'projectdjango12345@gmail.com'
    msg['To'] = email  # Get email from form input
    try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('projectdjango12345@gmail.com', 'fzxi ooyw owyk vakx')  # Use App Password
                smtp.send_message(msg)
                # books=BookRegistrationModel.objects.all()
                # return HttpResponse("<script>alert('Successfully Registered');window.location='adminindex';</script>")
    except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='registration';</script>")




    users=LoginModel.objects.all()
    return render(request,'Admin/statususer.html',{'users':users})




def list_book(request):    
    books=BookRegistrationModel.objects.all()
    return render(request,'Admin/list_book.html',{'books':books})

def editbooks(request,id):
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

        book_instance.save()
        # messages.success(request, "Book details updated successfully!")
        
        return redirect('/list_book')    

    obj=BookRegistrationModel.objects.get(Bid=id)
    
    context = {
    "data":obj,
    
    }
    
    return render(request,'Admin/editbook.html',context)


def deleteBook(request,id):
    obj=BookRegistrationModel.objects.get(Bid=id)
    obj.delete()
    return redirect('/list_book')  


def addbook(request):
    
    if request.method == 'POST':

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
        bookobj.Status = "Confirmed"
        bookobj.save()
    Category=CategoryModel.objects.all()
    return render(request,'Admin/addbook.html',{'Category':Category})
# end registration

# fill subcategories view
def fillSubcategory(request):
    did =int(request.POST.get("q"))
    sub=Sub_CategoryModel.objects.filter(Category=did).values()
    return JsonResponse(list(sub),safe=False)
# end view






def listsecond(request):
    books=secondhandBookModel.objects.all()
    return render(request,'Admin/listsecond.html',{'books':books})


def editsecond(request,id):
    if request.method=='POST':

        book_instance = get_object_or_404(secondhandBookModel,Secondid=id)
        book_name = request.POST.get("txt_bookname")
        category_id = request.POST.get('ddlCategory')
        year_input = request.POST.get("txt_year")
        print(year_input)
        if year_input:
            book_instance.year = year_input
        else:
            book_instance.year = None
        mrp = request.POST.get("MRP")
        price = request.POST.get("txt_price")
        language = request.POST.get("txt_Language")
        print(language)
        author = request.POST.get("txt_Author")
        edition = request.POST.get("Edition")
        publisher = request.POST.get("Publisher")
        book_image = request.FILES.get('book_file')
        
        # Update the book instance with the extracted data
        book_instance.BookName = book_name
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

        book_instance.save()
        # messages.success(request, "Book details updated successfully!")
        
        return redirect('/listsecond')    

    obj=secondhandBookModel.objects.get(Secondid=id)
    
    context = {
    "data":obj,
    
    }
    
    return render(request,'Admin/editsecond.html',context)
def deletesecond(request,id):
    obj=secondhandBookModel.objects.get(Secondid=id)
    obj.delete()
    return redirect('/listsecond') 

def addsecond(request):
    if request.method == 'POST':

        bookobj=secondhandBookModel()
        bookobj.BookName=request.POST.get("txt_bookname")
        category=CategoryModel.objects.get(CategoryId=request.POST.get('ddlCategory'))
        bookobj.maincategory=category    
       
        bookobj.noofpages=request.POST.get("txt_numberofpages")
        bookobj.MRP=request.POST.get("txt_MRP")
        bookobj.price=request.POST.get("txt_price")
        bookobj.year=request.POST.get("txt_year")
        
        bookobj.language=request.POST.get("txt_Language")
        bookobj.Author=request.POST.get("txt_Author")
        bookobj.Edition=request.POST.get("Edition")
        bookobj.Publisher=request.POST.get("Publisher")
        bookobj.Bookimg=request.FILES.get('book_file')
        bookobj.username = request.session.get('Uname')
        bookobj.Status = "Confirmed"
        bookobj.save()
    Category=CategoryModel.objects.all()
    return render(request,'Admin/addsecond.html',{'Category':Category})
# end registration

def Author_report(request):
    Author=LoginModel.objects.filter(Role='Author')
    return render(request,'Admin/Author_report.html',{'author':Author})
def deleteAuthor(request,id):
    Author=LoginModel.objects.get(LoginId=id)
    Author.delete()
    return redirect('/Author_report')    

def User_report(request):
    user=LoginModel.objects.filter(Role='Customer')
    return render(request,'Admin/User_report.html',{'user':user})
def deleteuser(request,id):
    user=LoginModel.objects.get(LoginId=id)
    user.delete()
    return redirect('/User_report')   


def pie_chart_sales(request):
    labels = []
    data = []

    # Aggregate sales per book (qty sold per book)
    queryset = tbl_Booking.objects.values('books__BookName').annotate(total_sales=Sum('qty'))

    for entry in queryset:
        labels.append(entry['books__BookName'])  # Assuming BookRegistrationModel has a field `BookName`
        data.append(entry['total_sales'])

    return render(request, 'Admin/piechart_sales.html', {
        'labels': labels,
        'data': data,
    })
class ExportExcelBook(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="booklist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Column 1', 'Column 2','Column 3']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = BookRegistrationModel.objects.all().values_list('BookName', 'numberofbooks','total_sales')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response



