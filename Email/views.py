from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import Profile
import uuid
from django.conf import settings
def home(request):
    return render(request, 'home.html')

def login_attemp(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request,'User not found, Plz create your account')
            return redirect('register')
        else:
            profile_obj = Profile.objects.filter(user=user_obj).first()
            if profile_obj.is_varified:
                user = authenticate(username=username , password= password)
                if user is None:
                   messages.success(request,'Please enter correct username or password') 
                else:
                    login(request, user)
                    messages.success(request,'You have successfully login ') 
                    return redirect('home')
            else:
                messages.success(request,'User is not varified plz check your mail')
                return redirect('login')

    return render(request, 'login.html')

def register_attemp(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

      
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is already taken')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request,'Email is already taken')
                return redirect('/register')

            user_obj = User(username=username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            token =str(uuid.uuid4())
            profile_obj =Profile.objects.create(user = user_obj , auth_token =token )
            profile_obj.save()
            send_mail_after_registation(email, token)
            return redirect('/token')
        except Exception as e:
            print(e)

    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request,'token_send.html')

def send_mail_after_registation(email , token):
    subject ='Your account need to be varified'
    message = f'Hi !! paste the link to varify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recpient_list = [email]
    send_mail(subject,message,email_from,recpient_list)

def verify(request , token):
    try:
        profile_obj = Profile.objects.filter(auth_token =token).first()
        if profile_obj:
            if profile_obj.is_varified:
                messages.success(request,'Your account have been already varified')
                return redirect('login')
            else:
                profile_obj.is_varified=True
                profile_obj.save()
                messages.success(request,'Your account have been varified')
                return redirect('login')
            
        else:
            return redirect('error')
    except Exception as e:
        print(e)

def error(request):
    return render(request, 'error.html')

