from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.userprofile, name = 'userprofile'),
    path('profile_edit/', views.profile_edit, name = 'profile_edit'),
    path('address/', views.address, name = 'address'),
    path('add_address/', views.add_address, name = 'add_address'),
    path('edit_address/<int:pk>/', views.edit_address, name = 'edit_address'),
    path('delete_address/<int:pk>/', views.delete_address, name = 'delete_address'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
]
