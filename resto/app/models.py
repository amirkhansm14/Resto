from django.db import models
from django.contrib.auth.models import User
# Create your models here.

    #for adding food
class Food(models.Model):
    foodname=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    price=models.IntegerField()
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to='food_images/')

class Staff(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phonenumber=models.CharField(max_length=15)
    category=models.CharField(max_length=50)
    password=models.CharField(max_length=128)

class Admin(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
   

class Tables(models.Model):
    number=models.IntegerField(unique=True)
    capacity=models.IntegerField()
    location=models.CharField(max_length=100)

class Orders(models.Model):
    table = models.ForeignKey(Tables, to_field='number', on_delete=models.CASCADE)
    foodname= models.CharField()
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)



