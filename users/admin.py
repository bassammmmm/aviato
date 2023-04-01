from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.



@admin.register(UserCustom)
class UserCustomAdmin(UserAdmin):
   model = UserCustom
   fieldsets = (       
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name', 'last_name','last_login','token', 'image', 'country', 'city', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                    'is_active', 'groups',
                                    'user_permissions')}),
    )
   add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'username',
                    'password1', 'password2')}
        ),
    )

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('image_tag', 'user')
    

admin.site.register(Address)