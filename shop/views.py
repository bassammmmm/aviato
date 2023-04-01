from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib import messages
from .forms import *
import random
import string
from django.contrib.sessions.models import Session
from users.models import *
from django.contrib.auth.decorators import login_required

def shop(request):
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    products = Product.objects.all()
    context = {
        'carts' : carts,
        'total_price' : total_price,
        'products': products
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'shop/shop.html', context)


def product(request, pk):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    product = Product.objects.get(pk = pk)
    images = ProductImages.objects.filter(product = product)
    related_products = Product.objects.filter(category=product.category).exclude(pk = pk)
    comments = Comment.objects.filter(product=product)
    number_of_comments = len(comments)
    context = {
        'product' : product,
        'images' : images,
        'related_products' : related_products,
        'comments' : comments,
        'number_of_comments' : number_of_comments,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    
    return render(request, 'shop/product.html', context)
    
@login_required(login_url= '/authentication/login/')
def add_to_cart(request, pk):
    user = request.user
    product = Product.objects.get(pk = pk)
    cart_exists = Cart.objects.filter(product = product, user_id = user.id)
    if cart_exists:
        control = 0
    else:
        control = 1

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if control == 0:
                cart = Cart.objects.get(product = product, user_id = user.id)
                cart.quantity = cart.quantity + quantity
                cart.save()
                messages.success(request, f"{quantity} of {cart.product.title} added to cart successfully.")
                return redirect('shop')
            elif control == 1:
                cart = Cart.objects.create(product = product, user_id = user.id, quantity = quantity)
                cart.save()
                messages.success(request, f"{quantity} of {cart.product.title} added to cart successfully.")
                return redirect('shop')
        else:
            messages.error(request, 'An error occurred.')
            return redirect('shop')
    else:
        if control == 0:
            cart = Cart.objects.get(product = product, user_id = user.id)
            cart.quantity = cart.quantity + 1
            cart.save()
            messages.success(request, f'{cart.product.title} added to cart successfully.')
            return redirect('shop')
        elif control == 1:
            cart = Cart.objects.create(product = product, user_id = user.id, quantity = 1)
            cart.save()
            messages.success(request, f'{cart.product.title} Added to cart successfully.')
            return redirect('shop')

@login_required(login_url= '/authentication/login/')
def cart(request):
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    if len(carts) == 0:
        return render(request, 'shop/empty_cart.html')
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
        
    context = {
        'carts' : carts,
        'total_price' : total_price
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'shop/cart.html', context)
        
@login_required(login_url= '/authentication/login/')
def remove_cart(request, pk):
    user = request.user
    cart = Cart.objects.get(pk = pk, user_id = user.id)
    cart.delete()
    return redirect('cart')

@login_required(login_url= '/authentication/login/')
def add_comment(request, pk):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            ip = request.META.get('REMOTE_ADDR')
            user = request.user
            product = Product.objects.get(pk = pk)
            comment_adding = Comment.objects.create(product = product, user_id = user.id, ip = ip, comment = comment)
            comment_adding.save()
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Error occurred')
            return redirect('product')
    return HttpResponseRedirect(url)

def random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@login_required(login_url= '/authentication/login/')
def checkout(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    user = request.user
    cart = Cart.objects.filter(user_id = user.id)
    coupon_id = request.session.get('coupon_id')
    coupon = Coupon.objects.filter(id=coupon_id).first()
    total = 0
    subtotal = 0
    shipping = 20
    for item in cart:
        total += item.total_items_price
        subtotal = total
    total = shipping + subtotal
    if coupon:
        total = total - (total * coupon.discount_percentage / 100) #* This is just to show the new price for the user
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid() and subtotal != 0:
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            phone = form.cleaned_data['phone']
            order_code = random_string(8).upper()
            ip = request.META.get('REMOTE_ADDR')
            order = Order()
            order.coupon = coupon
            order.total_price = total
            order.full_name = full_name
            order.address = address
            order.city = city
            order.country = country
            order.phone = phone
            order.code = order_code
            order.ip = ip
            order.user_id = user.id
            order.save()
            #* Make the cart into product items for the order.
            for item in cart:
                order_item = OrderItem()
                order_item.product = item.product
                order_item.user_id = user.id
                order_item.order = order
                order_item.quantity = item.quantity
                order_item.price = item.total_items_price
                order_item.min_price = item.product.min_price
                order_item.amount = item.product.amount
                order_item.save()
                product = Product.objects.get(pk = item.product.id)
                product.amount -= item.quantity 
                product.save()
                
            cart_deleting = Cart.objects.filter(user_id = user.id).delete()
            messages.success(request, 'Your order has been placed.')
            if coupon_id:
                request.session.pop('coupon_id')
            return redirect('home')

        else:
            messages.error(request, 'Error occurred. Make sure you enter valid information.')
            return redirect('checkout')
        
    context = {
        'cart' : cart,
        'total' : total,
        'subtotal' : subtotal,
        'shipping' : shipping,
        'total_price' : total_price,
        'carts' : carts,
    }

    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request,'shop/checkout.html', context)

@login_required(login_url= '/authentication/login/')
def orders(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    user = request.user
    orders = Order.objects.filter(user_id = user.id)
    context = {
        'orders' : orders,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'profiles/orders.html', context)


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(title__icontains = search)
        user = request.user
        carts = Cart.objects.filter(user_id = user.id)
        total_price = 0
        for cart in carts:
            total_price += cart.total_items_price
        context = {
            'carts' : carts,
            'total_price' : total_price,
            'products': products
        }
        #TODO This is just to show the profile in navbar:
        profile = UserCustom.objects.filter(pk = user.id).first()
        context['profile'] = profile
        #TODO
        return render(request, 'shop/shop.html', context)