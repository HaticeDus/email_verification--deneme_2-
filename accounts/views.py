from django.shortcuts import render,redirect
from django.contrib.auth.models import User # models import 
from django.contrib import messages #django messages from google
from .models import * # model * import all
import uuid # to get unique IDs for my Django objects
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import  login_required

@login_required(login_url='/')

def home(request):  #kullanıcıdan gelen isteği al 
    return render(request, 'home.html') #render fonk isteği ve html sayfasını gönder çıkan sonucu retun le geri döndür. rnder fonksiyonu html için kullanılır

def login_attempt(request):

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
    try:
        if user_obj is None:
            messages.success(request, '! User not found')
            return redirect('/login')

        profile_obj=Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
           messages.success(request, '! Profile is not verified check your mail')
           return redirect('/login')
        user=authenticate(username=username,password=password)
        if user is None:
           messages.success(request, '! Wrong password')
           return redirect('/login')
    except Exception as e:
        print(e)

        login(request,user) 
        return redirect('/') # home html sayfası çünkü url ismi '' 


    return render(request,'login.html')

def register_attempt(request):

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(password) #password is printed in terminal 
        
        if User.objects.filter(username=username).first():
         messages.success(request, '! Username is Already taken') #from django messages google
         return redirect('/register')

        if User.objects.filter(email=email).first():
         messages.success(request, '! Email is already  taken') #from django messages google
         return redirect('/register')    

        user_obj=User(username=username,email=email)
        user_obj.set_password(password)  
        user_obj.save() 
        auth_token=str(uuid.uuid4())
        profile_obj=Profile.objects.create(user=user_obj, auth_token=auth_token) #provides that randomly token adress each users.# profile_obj=Profile.objects.create(user=user_obj, token=get_random_token())
        profile_obj.save() #kullanıcıyı dbYe kaydetme 
             
        send_mail_after_registration(email,auth_token)#  return redirect('/token') #yönlendirme  
        return redirect('/token')      
            
    return render(request,'register.html')


def success(request):
    return render(request,'success.html')    

def token_send(request):
    return render(request,'token.html')


def verify(request, auth_token):
    try:
        profile_obj= Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj: 

            if profile_obj.is_verified:
                messages.success(request, '! Your account is already verified')
                return redirect('/login')


            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request, '! Email Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)        

def error_page(request):
    return render(request,'error.html')         

def send_mail_after_registration(email,token):
    subject='Your accounts need to be verified'
    message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]  #alıcı listesi
    send_mail(subject,message,email_from,recipient_list)
