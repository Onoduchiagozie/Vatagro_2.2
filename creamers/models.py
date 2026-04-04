from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CreamCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name


class CreamProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    category = models.ForeignKey(CreamCategory, on_delete=models.CASCADE, related_name="products")

    # no foreign key to other apps
    location = models.CharField(max_length=120, null=True, blank=True)

    # created_by if you want it
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="creamers_products"
    )

    def __str__(self):
        return self.name


class CreamRating(models.Model):
    product = models.ForeignKey(CreamProduct, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creamers_ratings")
    stars = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.stars} stars"

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.db.models import Avg
# from vatagro import settings
# from django.db import models
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
# # 1. Fixed User Manager
# class UserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, phone, client_status, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not first_name:
#             raise ValueError('Users must have a first name')
#
#         email = self.normalize_email(email)
#         user = self.model(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone,
#             client_status=client_status
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password, first_name="Admin", last_name="User", phone="0000",
#                          client_status="Admin"):
#         user = self.create_user(
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone,
#             client_status=client_status
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user
#
#
# # 2. Cleaned User Model
# class CreamerUser(AbstractBaseUser, PermissionsMixin):
#     # Basic Info
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
#     phone = models.CharField(max_length=20)
#
#     # Merged Profile Picture here (Cleaner than a separate Profile model)
#     profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')
#
#     # Relationship to Address (Assuming 'goods' app exists)
#     Active_Shipping_Address = models.ForeignKey(
#         'goods.ShippingAddress',
#         on_delete=models.SET_NULL,
#         blank=True, null=True
#     )
#
#     # Roles & Permissions
#     staff = models.BooleanField(default=False)  # Access to Django Admin
#     admin = models.BooleanField(default=False)  # Superuser status
#
#     # Business Logic
#     STATUS_CHOICES = (
#         ('Buyer', 'Buyer'),
#         ('Seller', 'Seller'),
#     )
#     client_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Buyer')
#
#     # Subscription Logic (For your Premium requirement)
#     is_premium = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'client_status']
#
#     objects = UserManager()
#
#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def __str__(self):
#         return self.email
#
#     # Required helper methods for Django Admin
#     @property
#     def is_staff(self):
#         return self.staff
#
#     @property
#     def is_superuser(self):
#         return self.admin
#
#     def has_perm(self, perm, obj=None):
#         return self.admin
#
#     def has_module_perms(self, app_label):
#         return self.admin
#
#
#  # Use this to refer to your User model
#
# # Centralized State List to keep code clean
# NIGERIAN_STATES = (
#     ("Abia", "Abia"), ("Adamawa", "Adamawa"), ("Akwa Ibom", "Akwa Ibom"),
#     ("Anambra", "Anambra"), ("Bauchi", "Bauchi"), ("Bayelsa", "Bayelsa"),
#     ("Benue", "Benue"), ("Borno", "Borno"), ("Cross River", "Cross River"),
#     ("Delta", "Delta"), ("Ebonyi", "Ebonyi"), ("Edo", "Edo"),
#     ("Ekiti", "Ekiti"), ("Enugu", "Enugu"), ("FCT - Abuja", "FCT - Abuja"),
#     ("Gombe", "Gombe"), ("Imo", "Imo"), ("Jigawa", "Jigawa"),
#     ("Kaduna", "Kaduna"), ("Kano", "Kano"), ("Katsina", "Katsina"),
#     ("Kebbi", "Kebbi"), ("Kogi", "Kogi"), ("Kwara", "Kwara"),
#     ("Lagos", "Lagos"), ("Nasarawa", "Nasarawa"), ("Niger", "Niger"),
#     ("Ogun", "Ogun"), ("Ondo", "Ondo"), ("Osun", "Osun"),
#     ("Oyo", "Oyo"), ("Plateau", "Plateau"), ("Rivers", "Rivers"),
#     ("Sokoto", "Sokoto"), ("Taraba", "Taraba"), ("Yobe", "Yobe"),
#     ("Zamfara", "Zamfara"),
# )
#
#
# class StoreLocation(models.Model):
#     name = models.CharField(max_length=50)
#     state = models.CharField(max_length=20, choices=NIGERIAN_STATES)
#     city = models.CharField(max_length=50)
#     # Fixed: 'default=True' on FK is invalid. Used null=True for safety.
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.name} - {self.city}"
#
#
# class ShippingAddress(models.Model):
#     state = models.CharField(max_length=50, choices=NIGERIAN_STATES)
#     city = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     is_active = models.BooleanField(default=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = "Shipping Addresses"
#
#     def __str__(self):
#         return f"{self.address}, {self.city}"
#
#
# class CreamerCategory(models.Model):
#     category_name = models.CharField(max_length=50)
#     slug = models.SlugField(max_length=100, unique=True)
#     cat_image = models.ImageField(upload_to='photos/category', blank=True)
#
#     class Meta:
#         verbose_name_plural = "Categories"
#
#     def __str__(self):
#         return self.category_name
#
#
# class CreamerProduct(models.Model):
#     MEASUREMENT_CHOICES = (
#         ('25 Litres', '25 Litres'),
#         ('50 Litres', '50 Litres'),
#         ('10 Litres', '10 Litres'),
#         ('25kg Bag', '25kg Bag'),
#         ('50kg Bag', '50kg Bag'),
#         ('Basket', 'Basket'),
#     )
#
#     product_name = models.CharField(max_length=255)
#     category = models.ForeignKey(CreamerCategory, on_delete=models.SET_NULL, null=True)
#     store_location = models.ForeignKey(StoreLocation, on_delete=models.SET_NULL, null=True, blank=True)
#
#     measurement = models.CharField(max_length=20, choices=MEASUREMENT_CHOICES)
#     product_description = models.TextField(blank=True, null=True)
#
#     # Changed to DecimalField for money (Integers cause math issues later)
#     price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
#     intra_state_shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     inter_state_shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#
#     prod_image = models.ImageField(upload_to='photos/goods')
#     stock = models.IntegerField(default=0)
#
#     # Renamed farmername to seller for consistency
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#
#     is_active = models.BooleanField(default=True)
#     date_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.product_name
#
#     def average_review(self):
#         # Local import to prevent circular error
#         from orders.models import ReviewRating
#         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
#         avg = 0
#         if reviews['average'] is not None:
#             avg = float(reviews['average'])
#         return avg
#
#
#
#
#
# class CreamerReviewRating(models.Model):
#     product=models.ForeignKey(CreamerProduct,on_delete=models.CASCADE)
#     creamuser=models.ForeignKey(User,on_delete=models.CASCADE)
#     subject=models.CharField(max_length=100,blank=True)
#     review=models.TextField(max_length=500,blank=True)
#     rating=models.FloatField()
#     status=models.BooleanField(default=True)
#     created_date=models.DateTimeField(auto_now_add=True)
#     update_at=models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.user)