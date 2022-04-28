from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models import Sum, Q

from tinymce.models import HTMLField
PAYMENT_TYPE = (
    ('a', 'Visa, Mastercard κτλ'),
    ('b', 'Τραπεζική Κατάθεση'),
    ('c', 'Μετρητά')
)

from frontend.models import PaymentMethod


class Customer(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    repeater = models.BooleanField(default=False)
    edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=220, verbose_name='Ονοματεπώνυμο')
    identity = models.CharField(max_length=220, verbose_name='ID', blank=True, null=True)
    phone = models.CharField(max_length=220, verbose_name='ΤΗΛΕΦΩΝΟ', blank=True, null=True)
    passport = models.CharField(max_length=220, verbose_name='ΔΙΑΒΑΤΗΡΙΟ', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name='ΗΜΕΡΟΜΗΝΙΑ ΓΕΝΝΗΣΗΣ')
    address = models.CharField(max_length=220, verbose_name='Διεύθυνση κατοικίας', blank=True, null=True)
    country = models.CharField(max_length=220, default='Ελλάδα', verbose_name='Εθνικότητα')
    email = models.EmailField(blank=True, null=True)
    notes = HTMLField(blank=True)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2, verbose_name='ΥΠΟΛΟΙΠΟ')

    class Meta:
        ordering = ['title']
    
    def save(self, *args, **kwargs):
        bookings = self.reservations.filter(checkIn=True)
        payments = self.payments.all()
        self.repeater = True if bookings.count() > 1 else False
        dept = bookings.aggregate(Sum('final_value'))['final_value__sum'] if bookings.exists() else 0
        payments = payments.aggregate(Sum('value'))['value__sum'] if payments.exists() else 0
        self.balance = dept - payments
        super(Customer, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_edit_url(self):
        return reverse('customers:update', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('customers:card', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('customers:delete', kwargs={'pk': self.id})

    @staticmethod
    def filter_qs(request, qs):
        q = request.GET.get('search_name', None)
        qs = qs.filter(Q(title__icontains=q) |
                       Q(email__icontains=q) |
                       Q(phone__icontains=q) |
                       Q(passport__icontains=q)
                       ) if q else qs
        return qs


class CustomerPayment(models.Model):
    title = models.CharField(max_length=220, verbose_name='Σημειώσεις', blank=True)
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    value = models.DecimalField(verbose_name='Ποσό',  max_digits=20, decimal_places=2)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='payments')
    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, null=True, blank=True, related_name='reservation_payments')
    date = models.DateField(default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'{self.customer} | {self.value}'
        super(CustomerPayment, self).save(*args, **kwargs)
        self.customer.save()
        if self.reservation:
            self.reservation.save()

    def __str__(self) -> str:
        return f'{self.customer} | {self.id}' if self.customer else f'No customer | {self.id}'

    def get_edit_url(self):
        return reverse('customers:payment_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('customers:payment_delete', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, qs):
        customer_name = request.GET.getlist('customer_name', None)
        check_in = request.GET.get('check_in', None)
        check_out = request.GET.get('check_out', None)
        qs = qs.filter(customer__id__in=customer_name) if customer_name else qs
        if check_in and check_out:
            qs = qs.filter(date__range=[check_in, check_out])
        return qs
