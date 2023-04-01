from django import forms
from .models import *


# class UserProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = UserProfile
#         fields = ['image', 'city', 'country', 'phone']
#         widgets = {
#             'city':forms.TextInput(attrs={'class':'form-control'}),
#             'country':forms.TextInput(attrs={'class':'form-control'}),            
#             'phone':forms.TextInput(attrs={'class':'form-control'}),   
#             'image': forms.FileInput(attrs={'class':'form-control'}),
#         }

class UserCustomForm(forms.ModelForm):
    class Meta:
        model = UserCustom
        fields = ['username','email','phone', 'image', 'city', 'country']
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control', 'readonly' : 'True'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control', 'readonly' : 'true'}),
            'city' : forms.TextInput(attrs={'class' : 'form-control'}),
            'country' : forms.TextInput(attrs= {'class' : 'form-control'}),
            'phone' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'image': forms.FileInput(attrs = {'class' : 'form-control',}),

            
        }
        
class AddressForm(forms.ModelForm):
    

    class Meta:
        model = Address
        fields = ('company', 'name', 'address', 'country', 'phone')
        
        widgets = {
            'company' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'name' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'address' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'country' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'phone' : forms.NumberInput(attrs = {'class' : 'form-control'}),

        }
        
        