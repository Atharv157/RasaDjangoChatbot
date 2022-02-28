from django.contrib import admin
from django.urls import path,include
from . views import *
urlpatterns = [
    path('',login_attempt, name = "login"),
    path('login',login_attempt, name = "login"),
    path('register',register_attempt, name = "register"),
    path('home',home,name="home"),
    path('logout',logout_user,name="logout"),
    path('interest_rates',interest_rates,name="interest_rates"),
]
