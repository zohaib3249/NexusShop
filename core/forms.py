from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import gettext_lazy as _
PAYMENT_CHOICES = (
    ('S', 'Card'),
    ('P', 'PayPal')
)

from allauth.account.forms import SignupForm    


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['email'] = forms.EmailField(label='E-mail')
class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Enter Name'),
        'class': 'form-control'
    }),required=True)
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': _('Email'),
        'class': 'form-control'
    }))
    
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('1234 Main St'),
        'class': 'form-control'
    }),required=True)
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': _('Phone Number'),
        'class': 'form-control'
    }))
    country = CountryField(blank_label=_('(select country)')).formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'

    }),required=True)
    

    oras = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': _('Town'),
        'class': 'form-control'
    }))

    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }),required=True)
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES ,required=True)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Promo code')
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
