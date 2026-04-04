from django.contrib import admin

from goods.models import  StoreLocation,Product,Category,ShippingAddress

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','store_location','measurment','quantity','farmername','prod_image','stock','is_active',)
    list_editable=('is_active','prod_image')
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name','states','city','created_by')
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('created_by','address','city','phone','state')
# Register your models here.



admin.site.register(StoreLocation,StoreAdmin)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ShippingAddress,ShippingAdmin)
