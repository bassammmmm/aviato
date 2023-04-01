from django.shortcuts import render, HttpResponse, redirect
from users.models import UserCustom
from django.contrib.auth.decorators import login_required
from shop.models import *
from .forms import ContactMessageForm
from .models import ContactMessage
from users.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site



def page_not_found(request, exception):
    return render(request, '404.html')

def home(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    trendy_products = Product.objects.filter(trendy=True)
        
    context = {
        'trendy_products' : trendy_products,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'home/home.html', context)


@login_required(login_url='/authentication/login')
def contact_me(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    context = {
        'carts' : carts,
        'total_price' : total_price
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            ip = request.META.get('REMOTE_ADDR')
            create = ContactMessage.objects.create(user_id = user.id, name = name, email = email, subject = subject, message = message, ip = ip)
            create.save()
            messages.success(request, 'We have received your message, we will reply to you via Email as soon as possible.')
            return redirect('contact_me')
        else:
            messages.error(request, 'Something went wrong. Make sure you enter valid data.')
            return redirect('contact_me')
    return render(request, 'contact_me.html', context)