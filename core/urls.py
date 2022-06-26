from django.urls import path


from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<str:id>/', add_to_cart, name='add-to-cart'),
    path('addtocart', addtocart, name='addtocart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<str:id>/', remove_from_cart, name='remove-from-cart'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<str:id>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('livraregratuita/', LivrareGratuita.as_view(), name='livraregratuita'),
    path('despre_noi/', DESPRE_NOI.as_view(), name='despre_noi'),
    path('contacteaza_ne/', CONTACTEAZA_NE.as_view(), name='contacteaza_ne'),
    path('cum_comand/', CUM_COMAND.as_view(), name='cum_comand'),
    path('ghid_de_marimi/', GHID_DE_MARIMI.as_view(), name='ghid_de_marimi'),
    path('newsletter/', NEWSLETTER.as_view(), name='newsletter'),
    path('politica_de_confidentialitate/', POLITICA_DE_CONFIDENTIALITATE.as_view(), name='politica_de_confidentialitate'),
    path('politica_de_retur/', POLITICA_DE_RETUR.as_view(), name='politica_de_retur'),
    path('termenii_si_conditiile/', TERMENII_SI_CONDITIILE.as_view(), name='termenii_si_conditiile'),
    path('product_info/<slug>/', CategoryView2.as_view(), name='category2'),
    path('send_email', send_email, name='send_email'),

    path('Received',PaymentReceivedTemplate, name='PaymentReceived'),
    path('addCoupon',addCoupon, name='addCoupon'),
    path('myaccount',myaccount, name='myaccount'),
    path('myorders',myorders, name='myorders'),
    path('refundorder',refundorder, name='refundorder'),
    path('addsubcriber',addsubcriber, name='addsubcriber'),
    path('adminUser',adminUser, name='adminUser'),
    path('getOrders',getOrders, name='getOrders'),
    path('filterItems',filterItems, name='filterItems'),
]


