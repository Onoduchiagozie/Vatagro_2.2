from django import forms
from account.models import User
from goods.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['product_name','product_catgeory','store_location','measurment','product_description','quantity','price','intra_state_shipping_fee','inter_state_shipping_fee','prod_image','stock']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'email', 'phone','client_status','Active_Shipping_Address']