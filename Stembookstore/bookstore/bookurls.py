
from django.urls import path,include
from . import views

urlpatterns = [
    path('index',views.index,name='index'),

    
    path('login',views.login,name='login'),
    path('',views.registration,name='registration'),
    path('filllocation',views.filllocation,name='filllocation'),

  
    
    path('search',views.search,name='search'),
    path('contact',views.contact,name='contact'),
    path('feedback',views.feedback,name='feedback'),
    path('newpassword',views.newpassword,name='newpassword'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('changepasswordset',views.changepasswordset,name='changepasswordset'),
     path('aboutus',views.aboutus,name='aboutus' ),

    path("secondhandbook",views.secondhandbook,name='secondhandbook'),
    path('listofsecondbooksview',views.listofsecondbooksview,name='listofsecondbooksview'),
    path('secondBookdetails/<id>',views.secondBookdetails,name='secondBookdetails'),
    path('CategoryBookdetails/<id>',views.CategoryBookdetails,name='CategoryBookdetails'),
    path('listofbooksview',views.listofbooksview,name='listofbooksview'),
    path('Bookdetails/<id>',views.Bookdetails,name='Bookdetails'),
    path('ownbooksview',views.ownbooksview,name='ownbooksview'),
    path('deletesecondBookdetails/<id>',views.deletesecondBookdetails,name='deletesecondBookdetails'),
    path('editsecondBookdetails/<id>',views.editsecondBookdetails,name='editsecondBookdetails'),
    path('buynow/<id>',views.buynow ,name='buynow'),



    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('update_cart/<item_id>/',views.update_cart,name='update_cart'),
    path('payment',views.makepayment,name='payment'),
    path('placeorder/<id>',views.placeorder,name='placeorder'),
    path('paymentdetails/<pid>',views.paymentdetails,name='paymentdetails'),
    path('bestsellers',views.bestsellers,name='bestsellers'),
]
