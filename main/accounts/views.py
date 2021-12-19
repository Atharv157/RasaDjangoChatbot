from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import * 
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.

@login_required(login_url='/')
def home(request):
    return render(request,'home.html')

def login_attempt(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email = email, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
            
        else:
            messages.success(request,"Invalid Credentials")
            return redirect('login')
    return render(request,'login.html')

def register_attempt(request):
    return HttpResponse("this functionality has been removed!!")
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if User.objects.filter(username=username).first():
#             messages.success(request,'Username is taken')
#             return redirect('/register')

#         if User.objects.filter(email=email).first():
#             messages.success(request,'Email is taken')
#             return redirect('/register')

#         user_obj = User.objects.create(username = username,email=email)
#         user_obj.set_password(password)
#         user_obj.save()

#         profile_obj = Profile.objects.create(user=user_obj)
#         profile_obj.save()

    # return render(request,'register.html')

def logout_user(request):
    auth.logout(request)
    return redirect('/login')







