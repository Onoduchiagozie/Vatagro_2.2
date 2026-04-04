from django.contrib import admin

# Register your models here.
from .models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','phone','staff','admin','client_status','Active_Shipping_Address')
    list_editable=('staff','admin')
admin.site.register(User,UserAdmin)

admin.site.register(Profile)


