# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.db.models import Q
#
# from goods.models import ShippingAddress
# from .models import CreamProduct,CreamCategory
#  # from .models import CreamProduct, CreamCategory, ShippingAddress
# from .serilaizers import ProductSerializer, CategorySerializer,ProductDetailSerializer
#
#
# # 1. List all Categories (Horizontal Scroll on Home)
# class CategoryListView(generics.ListAPIView):
#     queryset = CreamCategory.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.AllowAny]
#
# # 4. Single Product Detail
# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = CreamProduct.objects.filter(is_active=True)
#     serializer_class = ProductDetailSerializer
#     permission_classes = [permissions.AllowAny] # Allow viewing without login? Or change to IsAuthenticated
#     lookup_field = 'id' # We will find the product by its ID
#
#
#
# # 2. List All Products (General Grid)
# class ProductListView(generics.ListAPIView):
#     queryset = CreamProduct.objects.filter(is_active=True).order_by('-date_time')
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# # 3. "Closest" Products Logic (Based on State Matching)
# class NearbyProductListView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         user_addr = ShippingAddress.objects.filter(
#             created_by=self.request.user,
#             is_active=True
#         ).first()
#
#         if not user_addr:
#             return CreamProduct.objects.none()
#
#         return CreamProduct.objects.filter(
#             store_location__state=user_addr.state,
#             is_active=True
#         )
