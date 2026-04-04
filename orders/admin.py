from django.contrib import admin
from .models import OrderProducts, ReviewRating



class ReviewAdmin(admin.ModelAdmin):
    list_display=('user','product','rating','review')



admin.site.register(OrderProducts)
admin.site.register(ReviewRating,ReviewAdmin)