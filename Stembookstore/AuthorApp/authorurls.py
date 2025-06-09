from django.urls import path,include
from . import views
urlpatterns = [
   
    # path('bookregister',views.bookregister,name='bookregister'),
    path('Authorindex',views.Authorindex,name='Authorindex'),
    path('bookregistration',views.bookregistration,name='bookregistration'),
    path('fillSubcategory',views.fillSubcategory,name='fillSubcategory'),
    path('ownbooks',views.ownbooks,name='ownbooks'),
    path('editBookdetails/<id>',views.editBookdetails,name='editBookdetails'),
    path('deleteBookdetails/<id>',views.deleteBookdetails,name='deleteBookdetails'),
    path('viewpayment',views.Payment,name='viewpayment'),
    path('bydistrict/<int:district_id>',views.get_users_by_author,name='bydistrict'),
    #  path('bylocation/<int:location_id>',views.bylocation,name='bylocation'),
    
    path('viewdistrict',views.view_district),
    path('viewlocation',views.viewlocation,name='viewlocation'),
    path('bylocation/<int:location_id>',views.bylocation,name='bylocation'),
    path('ajax/rate/<int:product_id>/', views.ajax_rate_product, name='ajax_rate_product'),
    ]