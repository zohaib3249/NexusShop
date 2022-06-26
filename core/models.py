import email
from email.policy import default
from sys import intern
from turtle import title
from urllib import request
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from uuid import uuid4
import os
from django.db import connection
from django.contrib.auth.models import User
"""#Create the cursor
cursor = connection.cursor()

#Write the SQL code
sql_string = "CREATE  view vtable as SELECT * from core_order as od,core_billingaddress as ba, core_orderitem as oi,core_item as i where od.id=ba.billing_address_id and od.id=oi.id and oi.id=i.id"

#Execute the SQL
cursor.execute(sql_string)"""
def path_and_rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class Slide(models.Model):
    caption1_en = models.CharField(max_length=100,null=True,blank=True)
    caption2_en = models.CharField(max_length=100,null=True,blank=True)
    caption1_ro = models.CharField(max_length=100,null=True,blank=True)
    caption2_ro = models.CharField(max_length=100,null=True,blank=True)
    link = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(help_text="Size: 1920x570",null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_ae = models.BooleanField(default=True)
    
    def __str__(self):
        return "{} - {}".format(self.caption1_en, self.caption2_en)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    stock_no = models.CharField(max_length=10)
    Qty= models.IntegerField(default=0)  #total quantity of item when we add item in database
    rQty= models.IntegerField(default=0)  #remaining quantity of the item 
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    
    image = models.ImageField(upload_to=path_and_rename)
    image2 = models.ImageField(upload_to=path_and_rename)
    image3 = models.ImageField(upload_to=path_and_rename)
    is_active = models.BooleanField(default=True)
    addToHome = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def getItemPrice(self):
        if self.discount_price:
            return int(self.discount_price)
        else:
            return self.price
    def remainingPercents(self):
        return int((self.rQty/self.Qty)*100)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    size= models.CharField(max_length=50,default="M")

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    

    def get_total_item_price(self):
        return int(self.quantity * self.item.price)

    def get_total_discount_item_price(self):
        return int(self.quantity * self.item.discount_price)

    def get_amount_saved(self):
        return int(self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount_price:
            return int(self.get_total_discount_item_price())
        return int(self.get_total_item_price())


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20,null=True,blank=True)
    items = models.ManyToManyField(OrderItem,null=True,blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    mailSended = models.BooleanField(default=False)
    Shippingfee  = models.IntegerField(default=25)
    

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''
    
            
    def __str__(self):
        if self.get_total()>=100:
            self.Shippingfee=0
            self.save()
        else:
            self.Shippingfee=25
            self.save()
        return self.user.username
    
    def totalSave(self):
        if self.get_total()>=100:
            self.Shippingfee=0
            self.save()
        else:
            self.Shippingfee=25
            self.save()
        sum=0
        if self.items.count()>0:
        
            for orderItem in self.items.all():
                sum=sum+orderItem.item.price-orderItem.item.discount_price
        return int(sum)
        
    def get_total(self):
        total = 0
        if self.items:
            for order_item in self.items.all():
                total += order_item.get_final_price()
            if self.coupon:
                total -= self.coupon.amount
        return int(total)
    def grandTotal(self):
        
          
        return int(self.get_total()+self.Shippingfee)
class contactus(models.Model):
    name=models.CharField(max_length=25)
    subject=models.CharField(max_length=70)
    email=models.EmailField()
    message=models.CharField(max_length=255)
    def __str__(self):
        return self.subject

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    name = models.CharField(max_length=100,blank=True, null=True)
    email = models.CharField(max_length=100,blank=True, null=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.apartment_address

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField(default=0)
    min_amount = models.FloatField(default=0)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"




class NewsLetter(models.Model):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Subcribers(models.Model):
    email = models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email 
class SendNewsTOSUbcriber(models.Model):
    NewsLetter= models.ForeignKey(NewsLetter,on_delete=models.CASCADE)
    subcriber= models.ForeignKey(Subcribers,on_delete=models.CASCADE)
   
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.NewsLetter)+" send to "+str(self.subcriber)