from django.shortcuts import render, redirect
from users.models import UserCustom
from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.sites.shortcuts import get_current_site
from ecommerce import settings




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    value_of_username = request.POST['username']
                    messages.warning(request, 'You need to activate your account to login successfully, check your email.')
                    return render(request, 'authentication/login.html', {'value' : value_of_username})
            else:
                messages.error(request, 'Invalid username or password or account is not activated.')
                return redirect('login')
        else:
            messages.error(request, 'Please fill the empty fields.')
            return redirect('login')
    
    
    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        current_values = request.POST
        context = {
            'values' : current_values
        }
        if not last_name:
            messages.error(request, 'Last name is required.')
            return render(request, 'authentication/register.html', context)
        if not first_name:
            messages.error(request, 'First name is required.')
            return render(request, 'authentication/register.html', context)
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'authentication/register.html', context)
        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'authentication/register.html', context)
        if not password:
            messages.error(request, 'Password is required.')
            return render(request, 'authentication/register.html', context)
        if first_name and last_name and username and email and password:
            
            if UserCustom.objects.filter(username=username):
                messages.error(request, 'Try another username.')
                return render(request, 'authentication/register.html', context)
                
            elif UserCustom.objects.filter(email=email):
                messages.error(request, 'Try another email.')
                return render(request, 'authentication/register.html', context)
            
            elif (len(password) < 6):
                messages.error(request, 'Password is too short.')
                return render(request, 'authentication/register.html', context)
            
            else:
                token = str(uuid.uuid4())
                default_image = 'users/default_user.png'
                user = UserCustom.objects.create(username=username, email = email, token = token, first_name = first_name, last_name = last_name, image = default_image)
                user.set_password(password)
                user.is_active = False
                domain_name = get_current_site(request).domain
                verification_link = f"http://{domain_name}/authentication/verify/{token}/"
                subject = "Aviato Email Verification"
                message = f"Hello, {user.username}. click here {verification_link} to verify your account."
                email_sender = settings.EMAIL_HOST_USER
                email_receiver = [user.email]
                send_mail(subject, message, email_sender, email_receiver)
                user.save()
                messages.success(request, 'Your account has been created successfully, go to your Email to verify your account.')
                return redirect('login')
            
    return render(request, 'authentication/register.html')


def verify(request, token):
    user = UserCustom.objects.get(token = token)
    if user:
        if user.is_active:
            messages.warning(request, 'Link is expired or account is verified.')
            return render(request, 'authentication/verify.html')
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been verified successfully.')
            return render(request, 'authentication/verify.html')
        
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')
