from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from coupons.models import Coupon
from decimal import Decimal


class Category(models.Model):
    STATUS = (
        ('True' , 'True'),
        ('False' , 'False'),
    )
    status = models.CharField(choices=STATUS, max_length=20, blank=True, null = True)
    image = models.ImageField(blank = True, null = True, upload_to='images/')
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
class Product(models.Model):
    
    STATUS = [
        ('True', 'True'), #Available
        ('False', 'False') #Not Available
    ]
    
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products_images/')
    price = models.FloatField()
    amount = models.IntegerField()
    details = RichTextUploadingField()
    min_price = models.FloatField()
    description = models.CharField(max_length=255,)
    keywords = models.CharField(max_length=300,)
    status = models.CharField(choices=STATUS, default=True, max_length=100)
    favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale = models.CharField(max_length=20, blank = True, null = True, choices=STATUS, default = 'False')
    trendy = models.CharField(max_length=20, blank = True, null = True, choices=STATUS, default = 'False')
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe(f"<img src = '{self.image.url}' height = '50'/>")
    
    class Meta:
        ordering = ['-created_at']
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products_images/')
    
    class Meta:
        verbose_name = "Product Images"
        verbose_name_plural = "Products' Images"
        
    def __str__(self):
        return f"{self.product.title} Image"
    
    
class Comment(models.Model):
    STATUS = [
        ('New', 'New'),
        ('Read', 'Read')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ip = models.CharField(max_length=30, blank = True, null = True)
    status = models.CharField(choices = STATUS, blank = True, default = 'New', max_length = 20)
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    updated_at = models.DateTimeField(auto_now=True, blank = True)
    comment = models.TextField(blank=True, null=True, max_length = 1000)
    
    def __str__(self):
        return f"{self.user} Comment"
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    
    @property
    def total_items_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.product.title} * {self.quantity} for {self.user}"
    

class Order(models.Model):
    STATUS = [
        ('Processing' , 'Processing'),
        ('On Hold', 'On Hold'),
        ('Pending', 'Pending'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),

    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    code = models.CharField(max_length = 10, blank = True, null = True)
    full_name = models.CharField(max_length = 50, blank = True)
    city = models.CharField(max_length = 50, blank = True)
    country = models.CharField(max_length = 50, blank = True)
    address = models.CharField(max_length = 100, blank = True)
    phone = models.CharField(max_length = 100, blank = True, null = True)
    coupon = models.ForeignKey(Coupon, on_delete = models.SET_NULL, blank = True, null = True)
    total_price = models.FloatField(blank = True, null = True)
    ip = models.CharField(max_length = 30, blank = True)
    note = models.CharField(max_length=50, blank = True)
    status = models.CharField(choices=STATUS, max_length=20, default = 'Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Order"

class OrderItem(models.Model):
    STATUS = [
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    min_price = models.FloatField(blank=True, null=True)
    amount = models.IntegerField()
    min_amount = models.IntegerField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default = 'New', max_length=20)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.title} Order Item"
    
    @property
    def code(self):
        return self.order.code
    
    
    
    