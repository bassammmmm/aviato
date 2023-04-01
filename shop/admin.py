from django.contrib import admin
from .models import *
# Register your models here.


class ProductImagesInline(admin.TabularInline):

    model = ProductImages
    extra = 5

class ProductAdmin(admin.ModelAdmin):

    list_display = ('title', 'category', 'price', 'description', 'image_tag', 'amount')
    list_filter = ['category']
    inlines = [ProductImagesInline]

class CommentAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'comment', 'product', 'status']
    list_filter = ['status']
    readonly_fields = ['user', 'comment', 'ip', 'product', 'created_at', 'updated_at']
    ordering = ['-created_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'order', 'quantity', 'price', 'created_at', 'updated_at', 'user', 'amount', 'min_amount', 'min_price']
    
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''
    list_display = ['user', 'address']
    list_filter = ['user', 'status']
    readonly_fields = ['user', 'code', 'address', 'coupon', 'total_price', 'ip', 'created_at', 'updated_at', 'full_name', 'city', 'country', 'phone']
    search_fields = ['code']
    ordering = ['-created_at']
    inlines = [OrderItemInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)

