# from rest_framework import serializers
# from .models import CreamProduct, CreamCategory
# from rest_framework import serializers
# from django.contrib.auth import get_user_model, authenticate
#
# User = get_user_model()
#
#
# class RegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'client_status']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         # We use the create_user method we fixed earlier to handle hashing
#         user = User.objects.create_user(**validated_data)
#         return user
#
#
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')
#
#         if email and password:
#             user = authenticate(request=self.context.get('request'), email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError("Invalid email or password.")
#         else:
#             raise serializers.ValidationError("Must include 'email' and 'password'.")
#
#         data['user'] = user
#         return data
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CreamCategory
#         fields = ['id', 'category_name', 'slug', 'cat_image']
#
# class StoreLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreLocation
#         fields = ['id', 'name', 'state', 'city']
#
# class ProductSerializer(serializers.ModelSerializer):
#     # Retrieve the Category Name and Store Name directly
#     category_name = serializers.CharField(source='category.category_name', read_only=True)
#     store_state = serializers.CharField(source='store_location.state', read_only=True)
#     store_city = serializers.CharField(source='store_location.city', read_only=True)
#     seller_name = serializers.CharField(source='seller.full_name', read_only=True)
#     average_rating = serializers.FloatField(source='average_review', read_only=True)
#
#     class Meta:
#         model = CreamProduct
#         fields = [
#             'id', 'product_name', 'category', 'category_name',
#             'store_location', 'store_state', 'store_city',
#             'measurement', 'product_description', 'price',
#             'prod_image', 'stock', 'seller_name',
#             'average_rating', 'date_time'
#         ]
#
#
#
# class ProductDetailSerializer(serializers.ModelSerializer):
#     # Retrieve related names
#     category_name = serializers.CharField(source='category.category_name', read_only=True)
#     store_state = serializers.CharField(source='store_location.state', read_only=True)
#     store_city = serializers.CharField(source='store_location.city', read_only=True)
#     seller_name = serializers.CharField(source='seller.full_name', read_only=True)
#     seller_phone = serializers.CharField(source='seller.phone', read_only=True) # Good for contact
#     average_rating = serializers.FloatField(source='average_review', read_only=True)
#
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'product_name',
#             'category_name',
#             'store_state',
#             'store_city',
#             'measurement',       # <--- The size (e.g., 25kg Bag)
#             'price',
#             'stock',             # <--- The Available Quantity
#             'product_description',
#             'intra_state_shipping_fee',
#             'inter_state_shipping_fee',
#             'prod_image',
#             'seller_name',
#             'seller_phone',
#             'average_rating',
#             'date_time'
#         ]