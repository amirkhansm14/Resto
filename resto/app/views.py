from django.shortcuts import render,redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def tables(request):
    return render(request,'Tables.html')

def menu(request):
    foods =Food.objects.all()
    return render(request, 'menu.html', {'foods': foods})

def Login(request):
    return render(request,'Login.html')

def adminhome(request):
    return render(request,'Adminhome.html')
def addfood(request):
    if request.method== 'POST':
        fdname=request.POST['food_name']
        category=request.POST['category']
        price=request.POST['price']
        description=request.POST['description']
        image=request.FILES['food_image']
        data=Food.objects.create(foodname=fdname,category=category,price=price,description=description,image=image)
        data.save()
        return HttpResponse("succes")
    else:    
        return render(request,'Addfood.html')

def addstaff(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        category=request.POST['category']
        password=request.POST['password']
        data=Staff.objects.create(staffname=name,email=email,phonenumber=phone,category=category,password=password)
        data.save()
        a=Staff.objects.all()
        return render(request,'addstaff.html',{'a':a})
    else:
        a=Staff.objects.all()
        return render (request,'addstaff.html',{'a':a})
def staffdelete(request,id):
    book = get_object_or_404(Staff, id=id)
    book.delete()
    return redirect('addstaff') 
def Login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
    else:
        return render(request,'Login.html')