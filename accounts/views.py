from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required 

# Create your views here.

from django.db import IntegrityError
from django.contrib import messages,auth

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                # for unique username
                base_username = email.split('@')[0] # it seprate email before @
                username = base_username
                counter = 1
                while Account.objects.filter(username=username).exists(): # this condition check same user name is available in our bd or not
                    username = f"{base_username}{counter}"                # if exists then it add number with username
                    counter += 1

                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.phone_number = phone_number
                user.save()

                # user activation
                current_site = get_current_site(request)
                mail_subject = "Acivate Your accounts "
                message = render_to_string('accounts/account_verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.content_subtype = "html"
                send_email.send()

                # messages.success(request, "Registration successful! Please log in.")
                return redirect('/accounts/login/?command=verification&email='+email)
            except IntegrityError:
                messages.error(request, "This email or username already exists.")
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html',{'form':form})


from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        # Decode the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    # Check token validity
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('register')
    # return HttpResponse('OK')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = auth.authenticate(email=email, password=password)  # or email=email if backend supports it

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out.")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # user activation
            current_site = get_current_site(request)
            mail_subject = "Reseet Your Password "
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

            messages.success(request,'Password email has to be sent on Your Email Address')
            return redirect('login')
        else:
            messages.error(request,'Accounts Does not exists')
    return render(request,'accounts/forgotPassword.html')

def reset(request, uidb64, token):
    try:
        # Decode the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This is expired')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfully')
            return redirect('login')
        
        else:
            messages.error(request,'Both password must be same !')
            return redirect('reset_password')

    else:
        return render(request, 'accounts/reset_password.html')