from django import forms

from .models import Customer, CustomerPayment
from reservations.models import Reservation


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['balance', ]


class CustomerPaymentForm(BaseForm, forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    customer = forms.ModelChoiceField(required=True, queryset=Customer.objects.all(), widget=forms.HiddenInput())
    reservation = forms.ModelChoiceField(required=True, queryset=Reservation.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CustomerPayment
        fields = ['date', 'payment_type', 'value', 'customer', 'title', 'reservation']