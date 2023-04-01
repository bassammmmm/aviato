from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('verify/<str:token>/', views.verify, name = 'verify'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'authentication\password_reset.html'), name = 'password_reset'), #TODO Writing Email to send the password reset link
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'authentication\password_reset_done.html'), name ='password_reset_done'), #TODO A message saying that link is sent to the email.
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'authentication\password_reset_confirm.html'), name = 'password_reset_confirm'), #TODO This is a view to reset password (uidb64) is the user encoded for secure stuff
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'authentication\password_reset_complete.html'), name = 'password_reset_complete'), #TODO This message saying that password is reset successfully.
    path('logout/', views.logout, name = 'logout')
    
]
