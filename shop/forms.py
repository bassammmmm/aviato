from django import forms
from .models import *

class CartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        fields = ['quantity']
        
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'city', 'country', 'address', 'phone']

