from django.core import validators
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from django.urls import reverse
# Create your models here.


class User_Type(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Worker_Type(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Wage_Method(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)


class Login_Details(models.Model):
    u_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.EmailField(max_length=254)
    # read more how to apply as a password in forms.py
    password = models.CharField(max_length=50)
