from django.shortcuts import render,reverse,redirect,get_object_or_404
from .models import *
from django.http import *
from .forms import *
from django.utils.timezone import datetime
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os
from sendgrid import SendGridAPIClient
from django.conf import settings 
from sendgrid.helpers.mail import Mail
import smtplib
import csv
from django.http import HttpResponse

# Create your views here.

def sendgridmail(request):
    message = Mail(
    from_email='darshmishra3010@gmail.com',
    to_emails='darshmishra3010@gmail.com',
    subject='You have an Order',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return HttpResponseRedirect(reverse('home'))
    except Exception as e:
        return HttpResponse("not sent")

@login_required(login_url='ecommerce:customer_login')
def vendor_details(request,id):
    context={}
    context['vendor']=Vendor.objects.get(id=id)
    context['orders']=Order.objects.filter(order_vendor_name=Vendor.objects.get(id=id))
    context['items']=Item.objects.filter(item_vendor_name=Vendor.objects.get(id=id))
    return render(request,'vendor_details.html',context)

@login_required(login_url='clogin')
def customer_details(request,id):
    context={}
    cust9=[]
    allcust=Customer.objects.all()
    for cust in allcust:
        cust9.append(cust.customer_email)

    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)
    context['customer']=Customer.objects.get(id=id)
    context['orders']=Order.objects.filter(order_customer_name=Customer.objects.get(id=id))
    return render(request,'customer_details.html',context)

@login_required(login_url='clogin')
def myCart(request,id):
    context={}
    
    cust8=[]
    cust9=[]
    for c in Vendor.objects.all():
        cust8.append(c.vendor_email)
    for p in Customer.objects.all():
        cust9.append(p.customer_email)

    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)
    context['customerusers']=cust9
    context['vendorusers']=cust8
    context['customer']=Customer.objects.get(customer_email=request.user.email)
    try:
        orders=Cart.objects.get(cart_for=Customer.objects.get(id=id),cart_ordered='Not Ordered')
        context['orders']=orders
        return render(request,'myCart.html',context)#check same cart afterr adding
    except:
        cart=Cart()
        cart.cart_for=Customer.objects.get(customer_email=request.user.email)
        cart.cart_ordered='Not Ordered'
        cart.save()
        context['orders']=cart
    return render(request,'myCart.html',context)

def vendor_register(request):
    context={'register_form':vendorRegistrationForm()}
    context['message']=''
    if request.method=='POST':
        form=vendorRegistrationForm(request.POST)
        if form.is_valid():
             
             form.save()
             return HttpResponseRedirect(reverse('vendor_login'))

        else:
            context['message']='Something went wrong'
            return render(request,'vendor_register.html',context)
    else:
        return render(request,'vendor_register.html',context)
    
    return render(request,'vendor_register.html',context)


def vendor_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('vendor_details',args=[Vendor.objects.get(vendor_email=request.user.email).id]))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "vendor_login.html", context)
    else:
        return render(request, "vendor_login.html", context)

def customer_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('customer_details',args=[Customer.objects.get(customer_email=username).id]))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "customer_login.html", context)
    else:
        return render(request, "customer_login.html", context)

@login_required(login_url='clogin')
def sendmymail(request,id):
    v=Vendor.objects.get(id=id)
    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    s.login("mukeshmishra657@gmail.com","mishra@2001")
    message="You have an order"
    s.sendmail("mukeshmishra657@gmail.com",v.vendor_email,message)
    s.quit()
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='customer_login')
def add_item(request):
    context={}
    context={}
    cust8=[]
    cust9=[]
    for c in Vendor.objects.all():
        cust8.append(c.vendor_email)
    for p in Customer.objects.all():
        cust9.append(p.customer_email)

    context['customerusers']=cust9
    context['vendorusers']=cust8
    context['itemForm']=itemForm()
    context['message']=''
    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)
    username=request.user.username
    vendor=Vendor.objects.get(vendor_email=request.user.email)
    if request.method=='POST':
        form=itemForm(request.POST)
        if form.is_valid():
            i3=Item()
            i3.item_name=form.cleaned_data['item_name']
            i3.item_vendor_name=Vendor.objects.get(vendor_email=request.user.email)
            i3.item_cost=form.cleaned_data['item_cost']
            i3.item_description=form.cleaned_data['item_description']
            i3.item_quantity=form.cleaned_data['item_quantity']
            i3.item_status='Available'
            i3.save()
            return HttpResponseRedirect(reverse('vendor_details',args=[vendor.id]))
        else:
            context['message']='Something went wrong'
            return render(request,'additem.html',context)
    else:
        return render(request,'additem.html',context)
    return render(request,'additem.html',context)

@login_required(login_url='clogin')
def delete_item(request,id):
    i1=Item.objects.get(id=id)
    i1.delete()
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='clogin')
def home(request):
    context={}
    cust8=[]
    cust9=[]
    for c in Vendor.objects.all():
        cust8.append(c.vendor_email)
    for p in Customer.objects.all():
        cust9.append(p.customer_email)
    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)
    if request.user.email in cust8:
        context['vend']=Vendor.objects.get(vendor_email=request.user.email)

    context['customerusers']=cust9
    context['vendorusers']=cust8
    context['items']=Item.objects.all()
    return render(request,'home.html',context)

@login_required(login_url='clogin')
def item_details(request,id):
    context={}
    cust8=[]
    cust9=[]
    for c in Vendor.objects.all():
        cust8.append(c.vendor_email)
    for p in Customer.objects.all():
        cust9.append(p.customer_email)
    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)

    context['customerusers']=cust9
    context['vendorusers']=cust8
    context['item']=Item.objects.get(id=id)
    context['itemOrderForm']=itemOrderForm()
    if request.method=='POST':
        form=itemOrderForm(request.POST)
        if form.is_valid():
            o1=Order()
            o1.item_ordered=Item.objects.get(id=id)
            o1.order_quantity=form.cleaned_data['order_quantity']
            o1.order_customer_name=Customer.objects.get(customer_email=request.user.email)
            o1.order_vendor_name=o1.item_ordered.item_vendor_name
            if o1.order_quantity>o1.item_ordered.item_quantity:
                context['message']='Not available this much only '+str(o1.item_ordered.item_quantity)
                return render(request,'item_details.html',context)
            try:
                c1=Cart.objects.get(cart_for=Customer.objects.get(customer_email=request.user.email),cart_ordered='Not Ordered')
                c12=[]
                for order2 in c1.my_cart.all():
                    c12.append(order2.item_ordered.item_name)
                if o1.item_ordered.item_name in c12:
                    for order1 in c1.my_cart.all():
                        if order1.item_ordered.item_name==o1.item_ordered.item_name:
                            order1.order_quantity=order1.order_quantity+o1.order_quantity
                            order1.save()
                else:
                    o1.save()
                    c1.my_cart.add(o1)
                    c1.save()
            except:
                o1.save()
                c2=Cart()
                c2.cart_for=Customer.objects.get(customer_email=request.user.email)
                c2.save()
                c2.my_cart.add(o1)
                c2.save()
            
            return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))
        else:
            context['message']='Something went wrong'
            return render(request,'item_details.html',context)
    else:
        return render(request,'item_details.html',context)
    return render(request,'item_details.html',context)

@login_required(login_url='clogin')
def addToWishlist(request,id):
    item=Item.objects.get(id=id)
    cus1=Customer.objects.get(customer_email=request.user.email)

    if item in cus1.customer_wishlist.all():

        return HttpResponseRedirect(reverse('item_details',args=[id]))

    else:
        cus1.customer_wishlist.add(Item.objects.get(id=id))
        cus1.save()
    return HttpResponseRedirect(reverse('item_details',args=[id]))

@login_required(login_url='clogin')
def edit_customer_profile(request,id):
    context={}
    cus2=Customer.objects.get(id=id)
    context['edit_form']=customerEditForm()
    context['message']=''
    if request.method=='POST':
        form=customerEditForm(request.POST)
        if form.is_valid():
            cus2.customer_address=form.cleaned_data['customer_address']
            cus2.save()
            return HttpResponseRedirect(reverse('customer_details',args=[id]))
        else:
            context['message']='something is wrong'
            return render(request,'edit_customer.html',context)       
    else:
        return render(request,'edit_customer.html',context)

@login_required(login_url='clogin')
def edit_stock(request,id):
    i1=Item.objects.get(id=id)
    context={}
    context['item']=i1
    context['editStockForm']=editStockForm()
    if request.method=='POST':
        form=editStockForm(request.POST)
        if form.is_valid():
            i1.item_quantity=i1.item_quantity+form.cleaned_data['add_stock']
            i1.save()
            if i1.item_status=='Out Of Stock' and i1.item_quantity>0:
                i1.item_status='Available'
                i1.save()
            return HttpResponseRedirect(reverse('item_details',args=[id]))
    return render(request,'edit_stock.html',context)

@login_required(login_url='clogin')
def edit_item_image(request,id):
    i1=Item.objects.get(id=id)
    context={}
    context['edit_form']=itemImageEditForm()
    context['message']=''
    if request.method=='POST':
        form=itemImageEditForm(request.POST,request.FILES)
        if form.is_valid():
            file=request.FILES['item_image']
            i1.item_image=form.cleaned_data['item_image']
            i1.save()
            return HttpResponseRedirect(reverse('item_details',args=[id]))
        else:
            return render(request,'edit_item_image.html',context)
    else:
        return render(request,'edit_item_image.html',context)

@login_required(login_url='clogin')
def edit_customer_image(request,id):
    i1=Customer.objects.get(id=id)
    context={}
    context['edit_form']=customerImageEditForm()
    context['message']=''
    if request.method=='POST':
        form=customerImageEditForm(request.POST,request.FILES)
        if form.is_valid():
            file=request.FILES['customer_image']
            i1.customer_image=form.cleaned_data['customer_image']
            i1.save()
            return HttpResponseRedirect(reverse('customer_details',args=[id]))
        else:
            return render(request,'edit_customer_image.html',context)
    else:
        return render(request,'edit_customer_image.html',context)

@login_required(login_url='clogin')
def edit_vendor_image(request,id):
    i1=Vendor.objects.get(id=id)
    context={}
    context['edit_form']=vendorImageEditForm()
    context['message']=''
    if request.method=='POST':
        form=vendorImageEditForm(request.POST,request.FILES)
        if form.is_valid():
            file=request.FILES['vendor_image']
            i1.vendor_image=form.cleaned_data['vendor_image']
            i1.save()
            return HttpResponseRedirect(reverse('vendor_details',args=[id]))
        else:
            return render(request,'edit_vendor_image.html',context)
    else:
        return render(request,'edit_vendor_image.html',context)

@login_required(login_url='clogin')
def vendor_items(request):
    items=Item.objects.filter(item_vendor_name=Vendor.objects.get(vendor_email=request.user.email))
    context['items']=items
    return render(request,'myitems.html',context)

@login_required(login_url='clogin')
def order_delete(request,id):
    order_no=Order.objects.get(id=id)
    order_no.delete()
    return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))

@login_required(login_url='clogin')
def placecart(request,id):
    context={}
    
    final_price=0
    cus4=Customer.objects.get(customer_email=request.user.email)
    cart=Cart.objects.get(id=id)
    for order in cart.my_cart.all():
        final_price=final_price+order.item_ordered.item_cost*order.order_quantity
    context['final_price']=final_price    
    if request.method=='GET':
        if cus4.customer_money<=final_price:
            message="Please add "+"Rs."+str(final_price)+" to your Wallet "
            context['message']=message
            return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))
        else:
            for order in cart.my_cart.all():
                order.order_status='Order Placed'
                order.save()
                sendgridmail(request)
                #sendmymail(request,order.order_vendor_name.id)
                i5=Item.objects.get(id=order.item_ordered.id)
                i5.item_quantity=i5.item_quantity-order.order_quantity
                i5.item_sales=i5.item_sales+order.order_quantity
                i5.save()
                #sendmymail(request,order.order_vendor_name.id)

            cart.cart_ordered='Ordered'
            cart.save()
            cus4.customer_money=cus4.customer_money-final_price
            cus4.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))
    return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))

@login_required(login_url='clogin')
def addMoney(request):
    context={}
    cus5=Customer.objects.get(customer_email=request.user.email)
    context['addMoneyForm']=addMoneyForm()
    if request.method=='POST':
        form=addMoneyForm(request.POST)
        if form.is_valid():
            cus5.customer_money=cus5.customer_money+form.cleaned_data['amount']
            cus5.save()
    else:
        return render(request,'addmoney.html',context)
    return HttpResponseRedirect(reverse('myCart',args=[Customer.objects.get(customer_email=request.user.email).id]))
    

def customer_register(request):
    context={'register_form':vendorRegistrationForm()}
    context['message']=''
    if request.method=='POST':
        form=customerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('customer_login'))

        else:
            context['message']='Something went wrong'
            return render(request,'customer_register.html',context)
    else:
        return render(request,'customer_register.html',context)
    
    return render(request,'customer_register.html',context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('customer_login'))
    
def completeProfile(request):
    context={}
    context['completeProfileForm']=completeProfileForm()
    try:
        tp=Customer.objects.get(customer_email=request.user.email)
        return HttpResponseRedirect(reverse('customer_details',args=[Customer.objects.get(customer_email=request.user.email).id]))
    
    except:
        if request.method=='POST':
            form=completeProfileForm(request.POST)
            if form.is_valid():
                cus6=Customer()
                cus6.customer_name=request.user.first_name+' '+request.user.last_name
                cus6.customer_email=request.user.email
                cus6.customer_address=form.cleaned_data['ur_address']
                cus6.customer_contact=form.cleaned_data['ur_contact']
                cus6.save()
                return HttpResponseRedirect(reverse('customer_details',args=[Customer.objects.get(customer_email=request.user.email).id]))
            else:
                return render(request,'completeProfile.html',context)
        else:
            return render(request,'completeProfile.html',context)
                
    return render(request,'completeProfile.html',context)

@login_required(login_url='clogin')
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report-{}.csv"'.format(datetime.today().date())
    writer = csv.writer(response)
    writer.writerow(['Order ID','Item Ordered','Ordered By','Ordered On' ])

    orders=Order.objects.filter(order_vendor_name=Vendor.objects.get(vendor_email=request.user.email))

    for order in orders:
        row=[]
        row.append(order.id)
        row.append(order.item_ordered.item_name)
        row.append(order.order_customer_name)
        row.append(order.order_date)
        writer.writerow(row)

    return response

@login_required(login_url='clogin')
def myprofile(request):
    context={}
    
    cust8=[]
    cust9=[]
    for c in Vendor.objects.all():
        cust8.append(c.vendor_email)
    for p in Customer.objects.all():
        cust9.append(p.customer_email)
    if request.user.email in cust9:
        context['custom']=Customer.objects.get(customer_email=request.user.email)

    context['customerusers']=cust9
    context['vendorusers']=cust8
    if request.user.email in cust9:
        c10=Customer.objects.get(customer_email=request.user.email)
        return HttpResponseRedirect(reverse('customer_details',args=[c10.id]))
    
    if request.user.email in cust8:
        c11=Vendor.objects.get(vendor_email=request.user.email)
        return HttpResponseRedirect(reverse('vendor_details',args=[c11.id]))

def common_login(request):
    context={}
    return render(request,'login.html',context)

def edit_item(request,id):
    context={}
    context['item']=Item.objects.get(id=id)
    context['edit_form']=editItemForm()
    if request.method=='POST':
        form=editItemForm(request.POST)
        if form.is_valid():
            i7=Item.objects.get(id=id)
            i7.item_cost=form.cleaned_data['item_cost']
            i7.save()
        else:
            return render(request,'edit_item.html',context)
    else:
        return render(request,'edit_item.html',context)
    return HttpResponseRedirect(reverse('vendor_details',args=[Vendor.objects.get(vendor_email=request.user.email).id]))

def sendgridmail(request):
    message = Mail(
    from_email='darshmishra3010@gmail.com',
    to_emails='darshmishra3010@gmail.com',
    subject='You have an Order',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return HttpResponseRedirect(reverse('home'))
    except Exception as e:
        return HttpResponse("not sent")



