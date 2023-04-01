from django.urls import path
from . import views
urlpatterns = [
    path('', views.shop, name = 'shop'),
    path('product/<int:pk>/', views.product, name = 'product'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name = 'add_to_cart'),
    path('cart/', views.cart, name = 'cart'),
    path('remove_cart/<int:pk>/', views.remove_cart, name = 'remove_cart'),
    path('add_comment/<int:pk>/', views.add_comment, name = 'add_comment'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('orders/', views.orders, name = 'orders'),
    path('search/', views.search, name = 'search'),
]
