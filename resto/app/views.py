from django.shortcuts import render,redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum,Count,Min
# Create your views here.
def index(request):
    return render(request,'index.html')

def tables(request):
    a=Tables.objects.all()
    return render(request,'Tables.html',{'a':a})

def menu(request,id):
    a=id
    foods =Food.objects.all()
    order=(
        Orders.objects.filter(table__number=a)
        .values('Foodid__foodname')
        .annotate(
            first_order_id=Min('id'),
            quantity=Count('id'),
            total_price=Sum('total_amount')
        )
    )

    total = order.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(
        request,
        'menu.html',
        {
            'foods': foods,
            'a': a,
            'orders': order,
            'total': total
        }
    )

def orderdelete(request,id):
    Orders.objects.filter(id=id).delete()
   
    return redirect('order')

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
        return redirect('addfood')
    else:    
        a=Food.objects.all()
        return render(request,'Addfood.html',{'a':a})

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

def fooddelete(request,id):
    book = get_object_or_404(Food, id=id)
    book.delete()
    return redirect('addfood') 

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
               return redirect('cashier_dashboard')
            else:
                return redirect('kitchen_dashboard')
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
    
def Logout(request):
    auth.logout(request)
    return redirect('login')

def order(request):
    if request.method=='POST':
        table=request.POST.get('tbid')
        fd=request.POST.get('fdid')
        amount=request.POST.get('price')
        waiterid=request.user
        tbid=Tables.objects.get(id=table)
        fdid=Food.objects.get(id=fd)
        data=Orders.objects.create(table=tbid,Foodid=fdid,waiterid=waiterid,total_amount=amount)
        data.save()
        return redirect('menu', id=table)
    else:
        return redirect('menu', id=table)
    



def kitchen_dashboard(request):
    # Get all tables
    tables = Tables.objects.all()

    # Create a dictionary with orders grouped by table
    table_orders = []
    for table in tables:
        orders = (
            Orders.objects.filter(table=table)
            .values('Foodid__id', 'Foodid__foodname', 'status')
            .annotate(
                quantity=Count('id'),
                total_price=Sum('total_amount')
            )
        )
        table_orders.append({'table': table, 'orders': orders})

    context = {'table_orders': table_orders}
    return render(request, 'Kitchen.html', context)


def mark_ready(request, table_number, food_id):
    Orders.objects.filter(table__number=table_number, Foodid__id=food_id).update(status='ready')
    return redirect('kitchen_dashboard')

def cashier_dashboard(request):
    tables = Tables.objects.all()
    table_orders = []

    for table in tables:
        # Only ready orders for this table
        ready_orders = (
            Orders.objects.filter(table=table.number, status='ready')
            .values('Foodid__foodname', 'Foodid__price', 'Foodid__id')
            .annotate(
                quantity=Count('id'),
                total_price=Sum('total_amount')
            )
        )

        table_orders.append({
            "table": table,
            "ready_orders": list(ready_orders)
        })

    return render(request, "cashier_dashboard.html", {"table_orders": table_orders})





def bill_table(request, table_number):
    table = Tables.objects.get(number=table_number)

    # Get only READY orders for billing
    ready_orders = Orders.objects.filter(table=table_number, status="ready")

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")

        # Total only ready orders
        total_amount = ready_orders.aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        # Save the sale
        sale = Sales.objects.create(
            customer_name=customer_name,
            amount=total_amount
        )

        # Delete only ready orders after billing
        ready_orders.delete()

        return redirect("cashier_dashboard")

    # Bill preview before payment
    total = ready_orders.aggregate(total=Sum("total_amount"))["total"] or 0

    return render(request, "bill_page.html", {
        "table": table,
        "orders": ready_orders,
        "total": total
    })