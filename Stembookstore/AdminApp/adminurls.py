from django.urls import path,include
from AdminApp.views import *
from .views import *
urlpatterns = [
    path('district',district,name='district'),
    path('location',Location,name='location'),
    path('categoryView',categoryView,name='categoryView'),
    path('subcategoryView', subCategoryView,name='subcategoryView'),
    path('adminindex', adminindex,name='adminindex'),
    path('feedbackview',feedbackview,name='feedbackview'),
    path('deletefeedback/<id>',deletefeedback,name='deletefeedback'),
    path('statusbook',statusbook,name='statusbook'),
    path('changestatusbook/<id>',changestatusbook,name='changestatusbook'),
    path('statususer',statususer,name='statususer'),
     path('changestatususer/<id>',changestatususer,name='changestatususer'),
     path('list_book',list_book,name='list_book'),
     path('editbooks/<id>',editbooks,name='editbooks'),
     path('deleteBook/<id>',deleteBook,name='deleteBook'),
     path('addbook',addbook,name='addbook'),
     path('listsecond',listsecond,name='listsecond'),
     path('edisecond/<id>',editsecond,name='editsecond'),
     path('deletesecond/<id>',deletesecond,name='deletesecond'),
     path('addsecond',addsecond,name='addsecond'),
     path('Author_report',Author_report,name='Author_report'),
     path('deleteAuthor/<id>',deleteAuthor,name='deleteAuthor'),
     path('User_report',User_report,name='User_report'),
     path('deleteuser/<id>',deleteuser,name='deleteuser'),
     path('export_excel/', ExportExcelBook.as_view(), name='export_excel'),
    path('piechart_sales',pie_chart_sales,name='piechart_sales'),

]