import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    # For create user
    def create_user(self, first_name, last_name, email, password, role=None, phone_number=None, username=None):
        if not email:
            raise ValueError("Email field is required")
        if not password:
            raise ValueError("Password field is required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=role,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()
        return user

    # For create superuser
    def create_superuser(self, first_name, last_name, email, password, username=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_deleted = False
        user.save()
        return user


# This model is for Handling Users. This model replaced django's default auth.user model Changed username field to
# email for user login action.
class User(AbstractBaseUser, PermissionsMixin):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # Add a related_name argument to avoid clash with auth.User.groups
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',  # You can choose any meaningful name here
        related_query_name='user',
    )

    # Add a related_name argument to avoid clash with auth.User.user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',  # You can choose any meaningful name here
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'username']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined', 'username')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # return self.is_admin
        return True

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            return 'Vendor'
        elif self.role == 2:
            return 'Customer'


class Vendor(models.Model):
    COMPLETED = 1
    PARTIALLY_COMPLETED = 2
    BASICS_COMPLETED = 3

    PROFILE_STATUS = (
        (BASICS_COMPLETED, 'Basic Details Only'),
        (PARTIALLY_COMPLETED, 'In Completed Profile'),
        (COMPLETED, 'Completed Profile')
    )

    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=128, unique=True)
    email_id = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    contact_person_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_person_phone = models.EmailField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    updated_status = models.PositiveSmallIntegerField(
        choices=PROFILE_STATUS, blank=True, null=True, default=BASICS_COMPLETED
    )
    country = CountryField(default='IN')
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # ADD VERSATILE IMAGE FIELD, PPOIField

    company_logo = models.ImageField(upload_to='company_logos/')
    vendor_license = models.ImageField(upload_to='vendor_licenses/')

    class Meta:
        db_table = 'vendors_vendor'
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('user','email_id','company_name')

    def __str__(self):
        return self.company_name
    
class ProfileImage(models.Model):
    image = models.ImageField(upload_to='profile_images/')

    class Meta:
        db_table = 'profile_image'
        verbose_name = _('Profile Image')
        verbose_name_plural = _('Profile Images')

    def __str__(self):
        return str(self.image)