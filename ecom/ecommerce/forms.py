from django import forms
from .models import *
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm

class vendorRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    contact=forms.CharField(max_length=15,required=True)
    address=forms.CharField(max_length=200000,widget=forms.Textarea)

    class Meta:
        model=User
        fields=['first_name','last_name','address','email','contact','password1','password2']

    def save(self,commit=True):
        user=super(vendorRegistrationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.username=user.email
        
        if commit:
            user.save()
            v1=Vendor()
            v1.vendor_name=user.first_name+' '+user.last_name
            v1.vendor_address=self.cleaned_data['address']
            v1.vendor_email=user.email
            v1.vendor_contact=self.cleaned_data['contact']
            v1.save()
            
        
        return user


class customerRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    contact=forms.CharField(max_length=15,required=True)
    address=forms.CharField(max_length=200000,widget=forms.Textarea)

    class Meta:
        model=User
        fields=['first_name','last_name','address','email','contact','password1','password2']

    def save(self,commit=True):
        user=super(customerRegistrationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.username=user.email
        
        if commit:
            user.save()
            v1=Customer()
            v1.customer_name=user.first_name+' '+user.last_name
            v1.customer_address=self.cleaned_data['address']
            v1.customer_email=user.email
            v1.customer_contact=self.cleaned_data['contact']
            v1.save()
        
        return user

class itemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['item_name','item_description','item_cost','item_quantity']

class editItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['item_cost']

class itemOrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['order_quantity']

class customerEditForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['customer_address']

class stockEditForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['item_quantity']

class itemImageEditForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['item_image']

class customerImageEditForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['customer_image']

class vendorImageEditForm(forms.ModelForm):
    class Meta:
        model=Vendor
        fields=['vendor_image']

class addMoneyForm(forms.Form):
    amount=forms.IntegerField(min_value=0,max_value=20000)
    class Meta:
        model=Customer

class ImageForm(forms.Form):
    image=forms.ImageField()

class completeProfileForm(forms.Form):
    ur_address=forms.CharField(max_length=300)
    ur_contact=forms.CharField(max_length=15)

class editStockForm(forms.Form):
    add_stock=forms.IntegerField(min_value=1)