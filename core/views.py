import json
from multiprocessing import context
from threading import Thread
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.template import Context
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from requests import options
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category, Subcribers
from django.http import HttpResponseRedirect
from django.db.models.functions import *


from django.utils.translation import gettext_lazy as _
# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# email imports
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import *
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



class HomeView(ListView):
    
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True,addToHome=True)
    context_object_name = 'items'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an active order"))
            return redirect("/")


class ShopView(ListView):
    model = Item
    template_name ='shop.html'
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     option =self.request.GET.get('option')
    #     if option == "Pret: mic la mare" or option == "Price: small to large":
    #         context['ordering']= ['price']
    #     else:
    #         context['ordering'] = ['-price']
   
    #     return context

def PaymentReceivedTemplate(request):
    order = Order.objects.filter(user=request.user, ordered=True,mailSended=False).first()
    if order:
        
        if order.mailSended==False:
            
                t1=Thread(target=sendEmail_order_confirmation,args=(order,))
                t1.daemon=True
                t1.start()
                order.mailSended=True
                order.save()
           
                return render(request, 'paymentreceived.html', {'order': order})
    else:
        return redirect("/")
def sendEmail_order_confirmation(data):
    template= get_template('invoice.html').render({
        'order':data
    })
    email=EmailMessage(
        'Order Confirmation Email',
        template,
        settings.EMAIL_HOST_USER,
        [data.user.email] #hardd2014  user send email to user email ,email exist in order just type data.shipping_address.email
        )
    try:
        email.fail_silently=False
        email.content_subtype = "html"
        email.send()
        print("send")
        return JsonResponse(({"msg":"OK"}))
        
    except Exception as ex:
        print("Error",ex)
        return JsonResponse(({"msg":"ERROR"}))
def filterItems(request):
    ranged={"1":"price","2":"-price"}
    pricerange={"1":[0,10],"2":[10,20],"3":[20,50],"4":[50,100]}
    if request.method=="POST":
        data=json.loads(request.body)
        type=data['type']
        by=data['by']
        other=data['other']
        othervar=data['othervar']
       
        items=None
        if type=="ranged":
            if by=='0':
                if othervar=="0":
                    items=Item.objects.all()
                else:
                    items=Item.objects.filter(price__gte=pricerange[othervar][0],price__lte=pricerange[othervar][1]).order_by(ranged[by])
            else:
                if othervar=="0":
                    items=Item.objects.all().order_by(ranged[by])
                else:
                    items=Item.objects.filter(price__gte=pricerange[othervar][0],price__lte=pricerange[othervar][1]).order_by(ranged[by])
            html=render_to_string("ajaxTemplate.html",{"object_list":items})
            return JsonResponse({"data":html,'status':'ok'})
        else:
            if by!="0":
                if othervar=="0":
                    items=Item.objects.filter(price__gte=pricerange[by][0],price__lte=pricerange[by][1])
                else:
                    items=Item.objects.filter(price__gte=pricerange[by][0],price__lte=pricerange[by][1]).order_by(ranged[othervar])
                html=render_to_string("ajaxTemplate.html",{"object_list":items})
                return JsonResponse({"data":html,'status':'ok'})
            else:
                if othervar=="0":
                    items=Item.objects.all()
                else:
                    items=Item.objects.all().order_by(ranged[othervar])
                html=render_to_string("ajaxTemplate.html",{"object_list":items})
                return JsonResponse({"data":html,'status':'ok'})
    return JsonResponse({"data":"Error",'status':'error'})

def getOrders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=="POST":
            sortby=request.POST.get('sortby')
            fromd=request.POST.get('from')
            to=request.POST.get('to')
            if sortby !="all":
                orders= Order.objects.filter(ordered=True,ordered_date__gte=fromd,ordered_date__lte=to).order_by(sortby)
                being_delivered= Order.objects.filter(ordered=True,being_delivered=False,ordered_date__gte=fromd,ordered_date__lte=to).all().count()
                refund_requested= Order.objects.filter(ordered=True,refund_requested=True,refund_granted=False,ordered_date__gte=fromd,ordered_date__lte=to).all().count()
                delivered=Order.objects.filter(ordered=True,being_delivered=True,ordered_date__gte=fromd,ordered_date__lte=to).all().count()
                sum=0
                count=0
            
                for i in orders:
                    if i.ordered:
                        sum=sum+i.grandTotal()
                        count=count+1
                    
                    
                dict={"orders":orders,'count':count,'sum':sum,'being_delivered':being_delivered,'refund_requested':refund_requested,"delivered":delivered}
                return render(request,"admin.html", dict)
            else:
                return redirect("/adminUser")
        else:
            return redirect("/")
def adminUser(request):
    if request.user.is_authenticated and request.user.is_superuser:
        

        """ mo=Order.objects.annotate(
            month=TruncMonth('ordered_date'),
            year=TruncYear('ordered_date'),
        ).filter(ordered=True).values('month','year').distinct()
        print(mo)"""
        orders= Order.objects.filter(ordered=True)
        being_delivered= Order.objects.filter(ordered=True,being_delivered=False).all().count()
        refund_requested= Order.objects.filter(ordered=True,refund_requested=True,refund_granted=False).all().count()
        delivered=Order.objects.filter(ordered=True,being_delivered=True).all().count()
        sum=0
        count=0
    
        for i in orders:
            if i.ordered:
                sum=sum+i.grandTotal()
                count=count+1
            
            
        dict={"orders":orders,'count':count,'sum':sum,'being_delivered':being_delivered,'refund_requested':refund_requested,"delivered":delivered}
        return render(request,"admin.html", dict)
    else:
        return redirect("/")
def addsubcriber(request):
    if request.method=="POST":
        email=request.POST.get("email")
        if email:
            sub,created=Subcribers.objects.get_or_create(email=email)
            if created:
                messages.info(
                    request, _("Your email is added"))
            else:
                messages.info(request, _("Email already exist"))
        else:
            messages.warning(
                request, _("Email is required"))
    return redirect("/")
            
def send_email(request):
    
    if request.method=="GET":
        try:
            name=request.GET.get('name')
            uemail=request.GET.get('email')
            subject=request.GET.get('subject')
            message=request.GET.get('message')
            if name and uemail and subject and message:
                
                data={
                    "name":name,
                    "email":uemail,
                    "subject":subject,
                    "message":message,
                }
                
                template= get_template('send_email.html')
                context = {'data':data}
                template = template.render(context)
                email=EmailMessage(
                    'Message Received',
                    template,
                    settings.EMAIL_HOST_USER,
                    ['zohaib3249@gmail.com']#hardd2014
                    )
                try:
                    email.fail_silently=False
                
                    email.send()
                    print("send")
                    return JsonResponse(({"msg":"OK"}))
                    
                except Exception as ex:
                    print("Error",ex)
                    return JsonResponse(({"msg":"ERROR"}))
            else:
                return redirect("/")
        except Exception as ex:
            return redirect("/")
       
        
        
            

        
    else:
        print("re",request)
        return JsonResponse(({"msg":"GET Request not allowed"}))

class ItemDetailView(DetailView):
    model = Item
    template_name = "Category_temp2.html"


# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"
class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        
        order = Order.objects.get(user=self.request.user, ordered=False)
        
        if order.billing_address:
            context = {
                'order': order,
                'key':settings.STRIPE_PUBLIC_KEY,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, _("u have not added a billing address"))
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        
        
        order = Order.objects.get(user=self.request.user, ordered=False)
        for i in order.items.all():
            item=i.item
            item.rQty=item.rQty-i.quantity
            item.save()
            
    
        token = self.request.POST.get('stripeToken')
        amount = int(order.grandTotal() * 100)
        #4242 4242 4242 4242 use any code date and zip
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="RON",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.grandTotal()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            order.ref_code = create_ref_code()
            order.save()
            
            messages.success(self.request, "Order was successful")
            return redirect("/Received")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught  stripe.error.CardError as e
            print(e)
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, _("RateLimitError"))
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, _("Invalid parameters"))
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, _("Not Authentication"))
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, _("Network Error"))
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, _("Something went wrong"))
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(self.request, _("Serious Error occurred"))
            return redirect("/")


class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        option = self.request.GET.get('option')
        item = Item.objects.filter(category=category, is_active=True)
        if option == "Pret: mic la mare" or option == "Price: small to large":
            item = Item.objects.filter(category=category, is_active=True).order_by('price')
        if option == "Pret: mare la mic" or option == "Price: large to small":
            item = Item.objects.filter(category=category, is_active=True).order_by('-price')

        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, _("You do not have an active order"))
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                email = form.cleaned_data.get('email')
                name = form.cleaned_data.get('name')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                print(name,email)
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    name=name,
                    email=email,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, _("Invalid payment option select"))
                    return redirect('core:checkout')
            else:
                messages.warning(self.request, _("Please Fill Required Fields Correctly!"))
                return redirect('core:checkout')


        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an active order"))
            return redirect("core:order-summary")


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "index.html", context)
#
#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product-detail.html", context)
#
#
# def shop(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "shop.html", context)
def addCoupon(request):
    if request.method=="POST":
        data = json.loads(request.body)
        coupen=Coupon.objects.filter(code=data['code']).first()
        
        if coupen:
            
            check=Order.objects.filter(coupon__code=data['code'],user=request.user,ordered=True).first()
            if check==None:
                order=Order.objects.filter(id=data['orderID'],ordered=False).first()
                if order.coupon:
                    return JsonResponse({"msg":"Coupen is already used in this order","status":"error"})
                else:
                    
                    for order_item in order.items.all():
                        if order_item.item.discount_price:
                            return JsonResponse({"msg":"Coupen use only without discounted Items","status":"error"})
                    if order.get_total()>=coupen.min_amount:
                        order.coupon=coupen
                        order.save()
                        amount=order.get_total()
                        return JsonResponse({"msg":"Coupen Applied","status":"ok","amount":amount,"coupen":order.coupon.code})
                    else:
                        return JsonResponse({"msg":"Minmum Amount for this coupen is "+str(coupen.min_amount),"status":"error"})
            else:
                return JsonResponse({"msg":"Coupen is already used","status":"error"})
        else:
            return JsonResponse({"msg":"Invalid Code"})
    else:
        return JsonResponse({"msg":"Invalid Request","status":"error"})
def myorders(request):
    
    Orders= Order.objects.filter(user=request.user)
    sum=0
    count=0
    for i in Orders:
        if i.ordered:
            sum=sum+i.grandTotal()
            count=count+1
  
    dict={"orders":Orders,'count':count,'sum':sum}
    return render(request,"myorders.html",dict)
def refundorder(request):
    if request.method=="POST":
        orderid=request.POST.get('orderid')
        
        order=Order.objects.filter(id=orderid).first()
        if order:
                order.refund_requested= True
                order.save()
                messages.info(request, _("Applied for refund order"))
        else:
            messages.info(request, _("Order Not Found"))
        
    return redirect("core:myorders")
def myaccount(request):
    
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        if username and email and first_name and last_name:
            user=User.objects.get(id=request.user.id)
            if user:
                user.username=username
                user.email=email
                user.first_name=first_name
                user.last_name=last_name
                user.save()
                messages.info(request, _("Profile Updated"))
            else:
                messages.sucess(request, _("There is an error while updating your profile."))
        else:
            messages.error(request, _("All Fields are required please do not left blank."))
        return redirect("core:myaccount")
    return render(request,"myaccount.html")
def addtocart(request):
    if request.method=="POST":
        
        data = json.loads(request.body)
    
        item=Item.objects.filter(id=data["item_id"]).first()
        if item:
            if item.rQty>=int(data["Q"]):
                
                order_item, created = OrderItem.objects.get_or_create(
                    item=item,
                    user=request.user,
                   
                    size=data["size"],
                    ordered=False
                )
                order_qs = Order.objects.filter(user=request.user, ordered=False)
                if order_qs:
                    order = order_qs[0]
                    
                    if order.items.filter(id=order_item.id).exists():
                        order_item.quantity += 1
                        order_item.save()
                        qs = Order.objects.filter(user=request.user, ordered=False)
                        count=0
                        if qs.exists():
                            count=qs[0].items.count()
                        return JsonResponse({"item":item.title,"msg":"Item qty was updated.","count":count})
                    else:
                        order_item.quantity = 1
                        order_item.save()
                        order.items.add(order_item)
                        qs = Order.objects.filter(user=request.user, ordered=False)
                        count=0
                        if qs.exists():
                            count=qs[0].items.count()
                        return JsonResponse({"item":item.title,"msg":"Item qty was added.","count":count})
                    
                else:
                    
                    neworder = Order.objects.create(user=request.user)
                    neworder.items.add(order_item)
                    count=neworder.items.count()
                    return JsonResponse({"item":item.title,"msg":"Item was added to your cart","count":count})
            else:
                
                qs = Order.objects.filter(user=request.user, ordered=False)
                count=0
                if qs.exists():
                    count=qs[0].items.count()
                return JsonResponse({"item":item.title,"msg":"Item out of stock or select less than the remaining QTY "+str(item.rQty),"count":count})
        else:
            
            return JsonResponse({"item":"invalid Item","msg":"Error","count":-1})
    else:
         return JsonResponse({"item":"invalid Item","msg":"Invalid Request","count":-1})
@login_required
def add_to_cart(request,id):
   
    order_item = OrderItem.objects.get(id=id)
    print(order_item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(id=id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, _("Item qty was updated."))
            return redirect(f"core:order-summary")

        else:
            order_item.quantity = 1
            order_item.save()
            order.items.add(order_item)
            messages.info(request, _("Item was added to your cart."))
            view_name = request.GET.get('view')
            
            
            return redirect("core:order-summary")
    else:
        print("Not found")
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, _("Item was added to your cart."))
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, id):
    
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(id=id).exists():
            orderitem = OrderItem.objects.get(id=id)
            order.items.remove(orderitem)
            orderitem.delete()
            messages.info(request, _("Item was removed from your cart."))
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, _("Item was not in your cart."))
            return redirect("core:product")
    else:
        # add a message saying the user dosent have an order
        messages.info(request, _("u don't have an active order."))
        return redirect("core:product")
    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, id):
   
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(id=id).exists():
            orderitem = OrderItem.objects.get(id=id)
            
         
            if orderitem.quantity > 1:
                orderitem.quantity -= 1
                orderitem.save()
            else:
                order.items.remove(orderitem)
            messages.info(request, _("This item qty was updated."))
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, _("Item was not in your cart."))
            return redirect("core:product")
    else:
        # add a message saying the user dosent have an order
        messages.info(request, _("u don't have an active order."))
        return redirect("core:product")
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, _("This coupon does not exist"))
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, _("Successfully added coupon"))
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, _("You do not have an active order"))
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, _("Your request was received"))
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, _("This order does not exist"))
                return redirect("core:request-refund")





class LivrareGratuita(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "LivrareGratuita_temp.html", context)

class DESPRE_NOI(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "DESPRE_NOI_temp.html", context)

class CONTACTEAZA_NE(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "CONTACTEAZA_NE_temp.html", context)

class CUM_COMAND(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "CUM_COMAND_temp.html", context)
class GHID_DE_MARIMI(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "GHID_DE_MARIMI_temp.html", context)


class NEWSLETTER(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "NEWSLETTER_temp.html", context)

class POLITICA_DE_CONFIDENTIALITATE(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "POLITICA_DE_CONFIDENTIALITATE_temp.html", context)
class POLITICA_DE_RETUR(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "POLITICA_DE_RETUR_temp.html", context)

class TERMENII_SI_CONDITIILE(View):
    def get(self, *args, **kwargs):
        context = {}
        return render(self.request, "TERMENII_SI_CONDITIILE_temp.html", context)


class CategoryView2(DetailView):
    model = Item
    template_name = "Category_temp2.html"
