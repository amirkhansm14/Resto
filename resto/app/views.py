from django.shortcuts import render,redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
# Create your views here.
def index(request):
    return render(request,'index.html')

def tables(request):
    return render(request,'Tables.html')

def menu(request):
    return render(request,'Menu.html')

def Login(request):
    return render(request,'Login.html')

def adminhome(request):
    return render(request,'Adminhome.html')
def addfood(request):
    return render(request,'Addfood.html')