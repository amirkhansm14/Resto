from django.db import models

# Create your models here.

    #for adding food
class Food(models.Model):
    foodname=models.CharField()
    category=models.CharField()
    price=models.IntegerField()
    description=models.CharField()
    image=models.ImageField()

class Staff(models.Model):
    staffname=models.CharField()
    email=models.CharField()
    phonenumber=models.IntegerField()
    category=models.CharField()
    password=models.CharField()

class Admin(models.Model):
    name=models.CharField()
    email=models.CharField()
    password=models.CharField()

class Tables(models.Model):
    number=models.IntegerField()
    capacity=models.IntegerField()
    location=models.CharField()


    

