# from django.db import models
#
# from django.urls import path
# from . import apiView,authviews
#
# urlpatterns = [
#
#     path('api/register/', authviews.RegisterView.as_view(), name='api-register'),
#     path('api/login/', authviews.LoginView.as_view(), name='api-login'),
#
#     # Home Screen - All Products
#     path('products/', apiView.ProductListView.as_view(), name='api-products'),
#     path('products/<int:id>/', apiView.ProductDetailView.as_view(), name='api-product-detail'),
#     # Home Screen - Categories
#     path('categories/', apiView.CategoryListView.as_view(), name='api-categories'),
#     # Home Screen - Closest Products (Recommended)
#     path('products/nearby/', apiView.NearbyProductListView.as_view(), name='api-products-nearby'),
# ]