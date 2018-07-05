from __future__ import unicode_literals
from django.db import models
from apps.clothing_admin.models import *
import bcrypt

class UserManager(models.Manager):
    def validate_login(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        validEmail=True
        if len(postData['email'])==0:
            errors['login_email']='Email cannot be empty'
            validEmail=False
        elif not EMAIL_REGEX.match(postData['email']):
            errors['login_email']='Invalid email address'
            validEmail=False
        if validEmail:
            users=User.objects.filter(email=postData['email'])
            if len(users)==0:
                errors['login_main']='Login attempt failed'
            else:
                user=users[0]
                b=bcrypt.checkpw(postData['password'].encode(), user.password.encode())
                if not b:
                    errors['login_main']='Login attempt failed'
        return errors
    def validate_register(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']='First name cannot empty'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name cannot be empty'
        if len(postData['email'])<5:
            errors['reg_email']='Email address invalid'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email']='Email address invalid'
        elif len(User.objects.filter(email=postData['email']))>0:
            errors['reg_email']='An account is already registered to this email'
        if len(postData['password'])<8:
            errors['password']='Password must be atleast 8 characters in length'
        elif postData['password']!=postData['confirm']:
            errors['confirm']='Passwords do not match'
        return errors
        

class User(models.Model):
    user_level=models.IntegerField(default=1)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    claimed_shirt=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    password=models.CharField(max_length=255, null=True)
    cohort=models.ForeignKey(Cohort, related_name='students', null=True)
    objects=UserManager()

class Cart(models.Model):
    user=models.OneToOneField(User, primary_key=True, null=False)
    total=models.DecimalField(max_digits=9, decimal_places=2, default=0)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart, related_name='items')
    product=models.ForeignKey(Product, related_name='cart_items')
    color=models.ForeignKey(Color, related_name='cart_items')
    size=models.CharField(max_length=3, default='-')
    quantity=models.IntegerField()
    total=models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    # first_name=models.CharField(max_length=255)
    # last_name=models.CharField(max_length=255)
    # email=models.CharField(max_length=255)
    user=models.ForeignKey(User, related_name='orders', null=True)
    # cohort=models.CharField(max_length=255)
    # cohort=models.ForeignKey(Cohort, related_name='orders')
    total=models.DecimalField(max_digits=9, decimal_places=2)
    num_items=models.IntegerField(default=0)
    status=models.CharField(max_length=55, default='Unclaimed')
    location=models.ForeignKey(Location, related_name='orders', null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    ordered=models.BooleanField(default=False)
    batch=models.ForeignKey(Batch, related_name='orders', null=True)

class OrderItem(models.Model):
    product=models.ForeignKey(Product, related_name='orders')
    order=models.ForeignKey(Order, related_name='items')
    size=models.CharField(max_length=3)
    # color=models.CharField(max_length=100)
    color=models.ForeignKey(Color, related_name='order_items')
    quantity=models.IntegerField()
    total=models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now_add=True)



# Create your models here.
