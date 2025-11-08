from django.shortcuts import render,redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def tables(request):
    a=Tables.objects.all()
    return render(request,'Tables.html',{'a':a})

def menu(request):
    foods =Food.objects.all()
    return render(request, 'menu.html', {'foods': foods})

def cashier(request):
    return render(request,'Cashierhome.html')

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
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        category=request.POST['category']
        password=request.POST['password']
        data=User.objects.create_user(first_name=name,username=email,password=password)
        data.save()
        data1=Staff.objects.create(user_id=data,phonenumber=phone,category=category,password=password)
        data1.save()
        return redirect('addstaff')
    else:
        a=Staff.objects.all()
        return render (request,'Addstaff.html',{'a':a})

def staffdelete(request,id):
    book = get_object_or_404(Staff, id=id)
    book.delete()
    return redirect('addstaff') 

def log(request):
    if request.method=='POST':
        username=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if Staff.objects.filter(user_id=user).exists():
            login(request,user)
            a=Staff.objects.get(user_id=request.user.id)
            if a.category=='Dine In':
                return redirect('index')
            elif a.category=='Cashier':
               return redirect('cashierhome')
        elif Admin.objects.filter(user_id=user).exists():
            login(request,user)
            return redirect('adminhome')
        else:
           return render(request,'login.html',{'error':'user not found'})
    else:
        return render(request,'Login.html')
def addtables(request):
    if request.method=='POST':
        tableno=request.POST.get('table_number')
        capacity=request.POST.get('capacity')
        location=request.POST.get('location')
        data=Tables.objects.create(number=tableno,capacity=capacity,location=location)
        data.save()
        return redirect('addtable')
    else:
        a=Tables.objects.all()
        return render(request,'Addtables.html',{'a':a})