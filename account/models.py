from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth import get_user_model




class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    # FIX #1: Removed the stray bare `3` that was here between the two classes


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=20)
    Active_Shipping_Address = models.ForeignKey(
        'goods.ShippingAddress',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    # FIX #2: blank=True, null=True so registration doesn't require a photo
    profile_picture = models.ImageField(blank=True, null=True)

    STATUS = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),
    )
    client_status = models.CharField(max_length=500, choices=STATUS)

    USERNAME_FIELD = 'email'

    # FIX #3: REQUIRED_FIELDS is mandatory on AbstractBaseUser
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

    # FIX #4: Removed duplicate has_perm — original defined it twice,
    # silently dropping the first version (which checked is_admin)
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} Profile'


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    images=models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return  f'{self.user.first_name} Profile'
