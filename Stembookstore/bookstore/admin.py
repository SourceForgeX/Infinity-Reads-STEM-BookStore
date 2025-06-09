from django.contrib import admin
from .models import*
# Register your models here.
admin.site.register(LoginModel)
admin.site.register(RegisterModel)
admin.site.register(secondhandBookModel)
admin.site.register(CartItemModel)
admin.site.register(tbl_Booking)
admin.site.register(tbl_Booking_master)
admin.site.register(PaymentModels)
admin.site.register(FeedBackModel)
admin.site.register(BuyNowModel)
# admin.site.register(BookCategoryModel)

# admin.site.register(LanguageModel)