from django.db import models
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from register.models import User
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError

# Brand Model

class Brand(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='brand/')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendor_app_brand'
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def _str_(self):
        return self.name


# Category Model
class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='category/')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendor_app_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def _str_(self):
        return self.name


# Product Model
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/')
    display_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    class Meta:
        db_table = 'vendor_app_product'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def _str_(self):
        return self.name


# ProductSize Model
class ProductSize(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vendor_app_productsize'
        verbose_name = _('product size')
        verbose_name_plural = _('product sizes')

    def _str_(self):
        return self.name


class ProductAlternative(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    stock = models.IntegerField()

    class Meta:
        db_table = 'vendor_app_productalternative'
        verbose_name = _('product alternative')
        verbose_name_plural = _('product alternatives')

    def _str_(self):
        return self.product.name


# Cart Model
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_items = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'vendor_app_cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def _str_(self):
        return f"Cart {self.id}"


# CartItem Model
class CartItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_alternative = models.ForeignKey(ProductAlternative, on_delete=models.CASCADE)
    qty = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vir_app_cartitem'
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')

    def _str_(self):
        return f"CartItem {self.id}{self.cart}"

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alternative_name = models.CharField(max_length=100)
    house_name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    dist = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    alternative_phone = models.CharField(max_length=10 )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'models_address'
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return f"{self.house_name}, {self.dist}, {self.state}"

class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    review = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'models_testimonial'
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    

