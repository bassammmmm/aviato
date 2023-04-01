from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe



class UserCustom(AbstractUser):
    token = models.CharField(max_length=300, blank = True)
    image = models.ImageField(upload_to = 'profiles/', null = True)
    city = models.CharField(max_length=50, blank = True)
    country = models.CharField(max_length=50, blank = True)
    phone = PhoneNumberField(blank = True, null = False)


    def image_tag(self):
        return mark_safe(f"<img src = '{self.image.url}' height = '50' />")

    @property
    def full_name(self):
        
        return f"{self.first_name} {self.last_name}"
    

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length=50, blank = True, null = True)
    address = models.CharField(max_length = 255, null = True)
    country = models.CharField(max_length=25, null = True)
    phone = PhoneNumberField(null = True)
    country = models.CharField(max_length=25, null = True)
    company = models.CharField(max_length=60, null = True)
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = "Users' Addresses"
    
    def __str__(self):
        return f"{self.user} Address " 