from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path


urlpatterns = [
        path('',views.account,name='account'),
        path('dashboard',views.dashboard,name='dashboard'),


        path('<pk>/profile',views.UserUpdateView.as_view(),name='profile'),





        path('<pk>/UpdateShipping',views.ShippingAddressUpdateView.as_view(),name='shippingaddress'),
        path('createnewshipping',views.ShippingAddressCreateView.as_view(),name='newshippingaddress'),
        path('shippinglist',views.ShippingAddressListView,name='shippinglist'),


        path('purchasedproducts',views.MyPurchasedProducctsListView,name='purchasedproducts'),
        path('<pk>/orderupdate',views.FarmerOrderProductsUpdateView.as_view(),name='orderupdate'),



        path('storelist',views.StoreListView,name='storelist'),
        path('storeupdate/<pk>',views.StoreUpdateView.as_view(),name='storeupdate'),
        path('storecreate',views.StoreCreateView.as_view(),name='storecreate'),


        path('myproducts',views.MyProductsListView,name='myproducts'),
        path('newproducts',views.MyProductsCreateView.as_view(),name='newproducts'),
        path('<pk>/updateproducts',views.ProductsUpdateView.as_view(),name='updateproducts'),


        path('display_picture', views.Profile_Picture.as_view(), name='profile_picture'),

              ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)