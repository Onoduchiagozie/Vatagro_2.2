
from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user, get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from account.views import success
from farmer.forms import ProductForm, UserUpdateForm
from farmer.models import Cart, CartItem
from django.contrib.messages.views import SuccessMessageMixin
from goods.models import Product, ShippingAddress, StoreLocation
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView
from account.models import User,Profile
from orders.models import OrderProducts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# ACCOUNT LANDING PAGE
@login_required
def account(request):
    import datetime

    hour = datetime.datetime.now().hour
    greeting= ''
    if hour < 12:
        greeting = "Good morning"
    elif hour < 16:
        greeting = "Good afternoon"
    else:
        greeting = "Good Evening"



    pp=request.user
    account_status=''
    if request.user.is_staff and request.user.client_status == 'Seller':
        account_status='Merchant'
    elif request.user.client_status == 'Seller' or request.user.is_staff :
        account_status='Pending Authorization'
    elif request.user.client_status == 'Customer' and request.user.is_staff:
        account_status="You're a Staff But Not A Merchant"
    else:
        account_status='Customer'

    context = {
        'status':account_status,
        'greet':greeting,
        'pp':pp
    }

    return render(request, 'farmer/account.html', context)

def dashboard(request):
    total = 0
    total_year = 0
    total_month = 0
    total_week = 0
    year = OrderProducts.objects.filter(
        user=request.user, Transaction_date__gte=datetime.now(timezone.utc)-timedelta(days=365))
    day = OrderProducts.objects.filter(
        user=request.user, Transaction_date__gte=datetime.now(timezone.utc)-timedelta(days=1))
    week = OrderProducts.objects.filter(
        user=request.user, Transaction_date__gte=datetime.now(timezone.utc)-timedelta(days=7))
    month = OrderProducts.objects.filter(
        user=request.user, Transaction_date__gte=datetime.now(timezone.utc)-timedelta(days=30))
    year_count = year.count()
    month_count = month.count()
    week_count = week.count()
    # PRICE AMOUNT IN CERTAIN TIME PERIODS
    for x in year:
        total_year += x.amount
    for x in month:
        total_month += x.amount
    for x in week:
        total_week += x.amount

    # IF USER ==FARMER
    fulfiled_ordered = OrderProducts.objects.filter(
        status='Delivered', sold_by=request.user)
    unfulfiled_ordered = OrderProducts.objects.filter(
        sold_by=request.user).all().exclude(status='Delivered')

    unfulfil_count = unfulfiled_ordered.count()
    fulfiled_ordered_count = fulfiled_ordered.count()
    ful_ord_amount = 0
    unful_ord_amount = 0

    for x in fulfiled_ordered:
        ful_ord_amount += x.amount
    for x in unfulfiled_ordered:
        unful_ord_amount += x.amount

    total_order = fulfiled_ordered_count + unfulfil_count
    total_order_amount = ful_ord_amount+unful_ord_amount

    context = {
        'xr': week,
        'total': total,
        'total_week': total_week,
        'total_month': total_month,
        'total_year': total_year,
        'year': year_count,
        'month': month_count,
        'week': week_count,
        'fulfiled': fulfiled_ordered_count,
        'fop': ful_ord_amount,
        'unful': unfulfil_count,
        'uop': unful_ord_amount,
        'total_order': total_order,
        'total_order_amount': total_order_amount
    }

    return render(request, 'farmer/dashboard.html', context)

# UPDATE USER DETAILS

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class=UserUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'farmer/profile.html'
    def get_form_class(self):
        myform=super().get_form_class()
        myform.base_fields['Active_Shipping_Address'].limit_choices_to={'created_by':self.request.user}
        return myform

# UPDATE SHIPPING_ADDRESS
class ShippingAddressUpdateView(SuccessMessageMixin,UpdateView):
    model = ShippingAddress
    fields = ['state','city','address','phone','is_active']
    success_url = reverse_lazy('account')
    success_message = "Your Shipping Details Have Been Successfully Updated"
    template_name = 'farmer/shippingaddress.html'

# CREATE SHIPPING ADDRESS
class ShippingAddressCreateView(SuccessMessageMixin,CreateView):
    model = ShippingAddress
    fields = ['state','city','address','phone','is_active']
    success_url = reverse_lazy('account')
    template_name = 'farmer/NewShippingAddress.html'
    success_message = "You Have Successfully Added A New Shipping Address"
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# LIST SHIPPING ADDRESS
def ShippingAddressListView(request):
    my_shipping=ShippingAddress.objects.filter(created_by=request.user)
    context={
        'object':my_shipping
    }
    return render(request,'farmer/listshippingaddress.html',context)

# LIST MY_PRODUCTS
@login_required
def MyProductsListView(request):
    product=Product.objects.filter(farmername=request.user.id)
    context={
        'object':product
    }
    return render(request,'farmer/myproducts.html',context)

# CREATE MY PRODUCTS
class Profile_Picture(CreateView):
    model= Profile
    success_url = reverse_lazy('account')
    fields = ['images']
    template_name = "farmer/profile_picture.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


class MyProductsCreateView(SuccessMessageMixin,CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('account')
    success_message = "%(product_name)s Has Been Successfully Added To Your List Of Products"
    template_name = 'farmer/newmyproducts.html'
    def form_valid(self, form):
        form.instance.farmername = self.request.user
        return super().form_valid(form)

    def get_form_class(self):
        myform=super().get_form_class()
        myform.base_fields['store_location'].limit_choices_to={'created_by':self.request.user}
        return myform

# UPDATE PRODUCT DETAILS
class ProductsUpdateView(SuccessMessageMixin,UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('account')
    template_name = 'farmer/updateproducts.html'
    success_message = " Details For %(product_name)s Was Updated Successfully"

    def form_valid(self, form):
        form.instance.farmername = self.request.user
        return super().form_valid(form)

# LIST OF MY BOUGHT PRODUCTS & PRODUCTS BOUGHT FROM ME (as per dangote wey i be)

def MyPurchasedProducctsListView(request):
    products = OrderProducts.objects.filter(user=request.user)
    customer_bought_from_me = OrderProducts.objects.filter(sold_by=request.user).all().exclude(status='Delivered')
    context = {
        'object': products,
        'myobject': customer_bought_from_me,
    }
    return render(request, 'farmer/orderedproducts.html', context)

# UPDATE FARMER PRODUCT DELIVERY STATUS
class FarmerOrderProductsUpdateView(SuccessMessageMixin,UpdateView):
    model = OrderProducts
    fields = ['status', ]
    success_url = reverse_lazy('account')
    template_name = 'farmer/updateproducts.html'
    success_message = "Product Delivery Status Updated to %(status)s"

# CREATE STORE
class StoreCreateView(CreateView):
    model = StoreLocation
    fields = ['name','states','city']
    success_url = reverse_lazy('storelist')
    template_name = 'farmer/createnew.html'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# UPDATE STORE
class StoreUpdateView(UpdateView):
    model = StoreLocation
    fields = ['name','states','city']
    success_url = reverse_lazy('storelist')
    template_name = 'farmer/storeupdate.html'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# LIST OF STORE LOCATIONS
def StoreListView(request):
    my_store_list=StoreLocation.objects.filter(created_by=request.user)
    context={
        'object':my_store_list
    }
    return render(request,'farmer/storelist.html',context)
