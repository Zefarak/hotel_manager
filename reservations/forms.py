from django import forms
from django.core.exceptions import ValidationError
from dal import autocomplete

from .models import Reservation, Customer, ExtraCharge, Room


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class ReservationForm(BaseForm, forms.ModelForm):
    advance = forms.BooleanField(required=False, label='Δημιουργια Προκαταβολής')
    check_in = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=True,
        widget=autocomplete.ModelSelect2(url='reservations:auto_customers')
    )

    class Meta:
        model = Reservation
        fields = ['room', 'customer', 'source', 'check_in', 'check_out', 'capacity', 'clean_value',
                  'extra_cost_per_person', 'discount', 'advance'
                  ]

    def clean_check_out(self):
        check_in = self.cleaned_data['check_in']
        check_out = self.cleaned_data['check_out']
        if check_in > check_out:
            raise ValidationError('Invalid dates')
        return check_out


class ReservationCreateForm(ReservationForm):
    advance = forms.BooleanField(required=False, label='Δημιουργια Προκαταβολής')

    class Meta:
        model = Reservation
        fields = ['room', 'customer', 'source', 'check_in', 'check_out', 'capacity', 'clean_value',
                  'extra_cost_per_person', 'discount', 'advance'
                  ]

class ReservationUpdateForm(ReservationForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.HiddenInput())
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True, widget=forms.HiddenInput())


class ExtraChargeForm(BaseForm, forms.ModelForm):
    reservation = forms.ModelChoiceField(queryset=Reservation.objects.all(), required=True, widget=forms.HiddenInput())

    class Meta:
        model = ExtraCharge
        fields = '__all__'