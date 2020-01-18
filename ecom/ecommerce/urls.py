from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('vendor/<int:id>/details',views.vendor_details,name='vendor_details'),
    path('vendor/<int:id>/items',views.vendor_items,name='vendor_items'),
    path('item/<int:id>/details/editImage',views.edit_item_image,name='edit_item_image'),
    path('vendor/<int:id>/details/editImage',views.edit_vendor_image,name='edit_vendor_image'),
    path('customer/<int:id>/details/editImage',views.edit_customer_image,name='edit_customer_image'),
    #path('vendor/<int:id>/items/<int:id1>/details',views.vender_stock,name='vendor_stock'),
    path('item/<int:id>',views.item_details,name='item_details'),
    path('home/',views.home,name='home'),
    path('customer/<int:id>/details',views.customer_details,name='customer_details'),
    path('customer/<int:id>/myCart',views.myCart,name='myCart'),
    path('vendor/login',views.vendor_login,name='vendor_login'),
    path('customer/login',views.customer_login,name='customer_login'),
    path('vendor/register',views.vendor_register,name='vendor_register'),
    path('customer/register',views.customer_register,name='customer_register'),
    path('customer/wishlist/<int:id>',views.addToWishlist,name='wishlist'),
    path('customer/<int:id>/details/edit',views.edit_customer_profile,name='edit_customer_profile'),
    path('item/<int:id>/details/editstock',views.edit_stock,name='edit_stock'),
    path('customer/myCart/delete/<int:id>',views.order_delete,name='order_delete'),
    path('customer/myCart/<int:id>/placecart',views.placecart,name='place_cart'),
    path('customer/addmoney',views.addMoney,name='addMoney'),
    path('vendor/item/add',views.add_item,name='add_item'),
    path('logout',views.user_logout,name='logout'),
    path('sendmymail',views.sendmymail,name='sendmymail'),
    path('customer/completeprofile',views.completeProfile,name='completeProfile'),
    path('vendor/records',views.export_to_csv,name='export_to_csv'),
    path('myProfile',views.myprofile,name='myprofile'),
    path('',views.common_login,name='clogin'),
    path('item/<int:id>/details/edit',views.edit_item,name='edit_item'),
    path('item/<int:id>/delete',views.delete_item,name='delete_item'),
    path('sendgridmail/',views.sendgridmail,name='sendgridmail')
]

if settings.DEBUG: 
    urlpatterns += static('/media/', 
    document_root='/media/') 
