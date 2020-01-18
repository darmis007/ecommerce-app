from django.db import models
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# Create your models here.

class Vendor(models.Model):
    vendor_name=models.CharField(max_length=100,blank=True,null=True)
    vendor_address=models.CharField(max_length=300,blank=True,null=True)
    vendor_contact=models.CharField(max_length=15,blank=True,null=True)
    vendor_email=models.EmailField(blank=True,null=True,max_length=300)
    vendor_image=models.ImageField(upload_to ='vendor/displaypic',blank=True,null=True)
    vendor_money=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.vendor_name}'
        

class Item(models.Model):
    item_name=models.CharField(max_length=200)
    item_vendor_name=models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True,blank=True)
    item_description=models.TextField(max_length=2000,null=True,blank=True)
    item_cost=models.PositiveIntegerField(blank=True,null=True)
    item_image=models.ImageField(upload_to ='items/displaypic',blank=True,null=True)
    item_status=models.CharField(max_length=200,choices=(('Available','Available'),('Out Of Stock','Out Of Stock')))
    item_quantity=models.PositiveIntegerField(default=0)
    item_sales=models.PositiveIntegerField(default=0)

    class Meta:
        ordering=['item_sales']


class Customer(models.Model):
    customer_name=models.CharField(max_length=100)
    customer_address=models.TextField(max_length=2000)
    customer_contact=models.CharField(max_length=15,null=True,blank=True)
    customer_email=models.EmailField(blank=True,null=True)
    customer_money=models.BigIntegerField(default=0,null=True,blank=True)
    customer_wishlist=models.ManyToManyField(Item,related_name='myWishlist')
    customer_image=models.ImageField(upload_to ='customer/displaypic',blank=True,null=True)

    def __str__(self):
        return f'{self.customer_name}'
    

class Order(models.Model):
    item_ordered=models.ForeignKey(Item,on_delete=models.CASCADE)
    order_quantity=models.PositiveIntegerField(default=1)
    order_vendor_name=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_customer_name=models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now=True)
    order_status=models.CharField(max_length=200,choices=(('In Cart','In Cart'),('Order Placed','Order Placed'),('In Transit','In Transit'),('Delivered','Delivered')),default='In Cart')

    def __str__(self):
        return f'{self.item_ordered}  {self.order_quantity}'
    


class Cart(models.Model):
    cart_for=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    my_cart=models.ManyToManyField(Order,related_name='myCart')
    cart_created_date=models.DateField(auto_now=True)
    cart_created_time=models.TimeField(auto_now=True)
    cart_ordered=models.CharField(max_length=20,choices=(('Ordered','Ordered'),('Not Ordered','Not Ordered')),default='Not Ordered')

    def __str__(self):
        return f'{self.cart_for} Cart {self.id}'
        
