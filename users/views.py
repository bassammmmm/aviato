from django.shortcuts import render, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, render
from shop.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url= '/authentication/login/')
def userprofile(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    profile = UserCustom.objects.get(pk = user.id)
    context = {
        'profile' : profile,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'profiles/profile.html', context)

@login_required(login_url= '/authentication/login/')
def profile_edit(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    user = request.user
    current_profile = UserCustom.objects.get(id = user.id)
    form = UserCustomForm(instance=current_profile)

    context = {
        'form' : form,
        'current_profile' : current_profile,
        'total_price' : total_price,
        'carts' : carts,
    }
    
    
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    
    
    if request.method=='POST':
        form = UserCustomForm(request.POST, request.FILES, instance = current_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully.')
            return redirect('userprofile')
        else:
            messages.error(request, 'Failed to update your profile, please enter valid data.')
            return redirect('profile_edit')
        
    return render(request, 'profiles/profile_edit.html', context)

@login_required(login_url= '/authentication/login/')
def address(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    addresses = Address.objects.filter(user = user)
    context = {
        'addresses' : addresses,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'profiles/address.html', context)

@login_required(login_url= '/authentication/login/')
def add_address(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    user = request.user
    addresses = Address.objects.filter(user = user)
    form = AddressForm()
    context = {
        'form' : form,
        'addresses' : addresses,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']
            company = form.cleaned_data['company']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            creation = Address.objects.create(country=country, company=company, address=address, phone=phone, name=name, user=user)
            creation.save()
            messages.success(request, 'Address added successfully.')
            return redirect('address')
        else:
            messages.error(request, 'Please enter valid data.')
            return redirect('add_address')
    return render(request, 'profiles/add_address.html', context)

@login_required(login_url= '/authentication/login/')
def edit_address(request, pk):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    address = Address.objects.get(pk = pk)
    form = AddressForm(instance = address)
    context = {
        'form' : form,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    if request.method == 'POST':
        form = AddressForm(request.POST, instance = address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('address')
        else:
            messages.error(request, 'Failed to update your address.')
            return redirect('address')
    
    return render(request, 'profiles/edit_address.html', context)

@login_required(login_url= '/authentication/login/')
def delete_address(request, pk):
    address = Address.objects.get(pk = pk)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('address')

def dashboard(request):
    #TODO This is just to show profile cart in navbar:
    user = request.user
    profile = UserCustom.objects.filter(pk = user.id).first()
    #TODO

    #TODO This is just to show user's cart in navbar:
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price = total_price + cart.total_items_price
    #TODO
    
    orders = Order.objects.filter(user_id = user.id, status='Completed')
    context = {
        'profile': profile,
        'total_price' : total_price,
        'orders' : orders,
    }
    return render(request, 'profiles/dashboard.html', context)