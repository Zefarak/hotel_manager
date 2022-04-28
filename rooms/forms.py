from django import forms

from .models import Room, RoomPrice, RoomCharge


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RoomForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['extra_charges']


class RoomPriceForm(BaseForm, forms.ModelForm):
    date_start = forms.DateField(required=True, label='ΑΠΟ', widget=forms.DateInput(attrs={'type': 'date'}))
    date_end = forms.DateField(required=True, label='ΕΩΣ', widget=forms.DateInput(attrs={'type': 'date'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = RoomPrice
        fields = '__all__'
        exclude = ['price']


class RoomPriceForm_(BaseForm, forms.ModelForm):
    date_start = forms.DateField(required=True, label='ΑΠΟ', widget=forms.DateInput(attrs={'type': 'date'}))
    date_end = forms.DateField(required=True, label='ΕΩΣ', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RoomPrice
        fields = '__all__'
        exclude = ['minimum_days', 'price']


class RoomChargeForm(BaseForm, forms.ModelForm):

    class Meta:
        model = RoomCharge
        fields = '__all__'

