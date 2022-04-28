from django.db import models
from django.urls.base import reverse
from django.db.models import Q, Sum

from itertools import chain
# Create your models here.

from customers.models import Customer, CustomerPayment
from rooms.models import Room
from .managers import ReservationManager
import datetime
from frontend.tools import initial_date

SOURCES = (
        ('a', 'WebHotelier'),
        ('g', 'Airbnb'),
        ('w', 'Booking'),
        ('b', 'Social Media'),
        ('c', 'Email'),
        ('d', 'Τηλεφωνο'),
        ('e', 'Site'),
        ('f', 'Αλλο')
    )


class Reservation(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='bookings')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='reservations', verbose_name='ΠΕΛΑΤΗΣ')
    source = models.CharField(max_length=1, choices=SOURCES, default='a')
    check_in = models.DateField()
    check_out = models.DateField()
    checkIn = models.BooleanField(default=False)
    isCancel = models.BooleanField(default=False, verbose_name='ΑΚΥΡΩΜΕΝΗ')
    isDone = models.BooleanField(default=False, verbose_name='ΟΛΟΚΛΗΡΩΜΕΝΗ')

    capacity = models.IntegerField(default=1, verbose_name='GUEST')

    clean_value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='TOTAL ROOM COST')
    extra_cost_per_person = models.DecimalField(decimal_places=2, max_digits=20, default=0,
                                                verbose_name='EXTRA BED')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='Total Value')
    charges_value = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='ΕΠΙΠΛΕΟΝ ΧΡΕΩΣΕΙΣ')
    discount = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='DISCOUNT')
    days = models.IntegerField(default=1)
    payment_value = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    final_value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='ΑΞΙΑ')

    objects = models.Manager()
    my_query = ReservationManager()

    class Meta:
        ordering = ['-check_in', 'checkIn']

    def save(self, *args, **kwargs):
        if self.checkIn:
            self.isCancel = False
        payment_qs = self.reservation_payments.all()
        print(payment_qs)
        self.payment_value = payment_qs.aggregate(Sum('value'))['value__sum'] if payment_qs.exists() else 0
        self.value = self.clean_value + self.extra_cost_per_person
        self.charges_value = self.extra_charges.aggregate(Sum('final_value'))['final_value__sum'] if self.extra_charges.exists() else 0
        self.final_value = self.value + self.charges_value
        super().save(*args, **kwargs)
        if self.room:
            self.room.save()
        if self.customer:
            self.customer.save()

    def __str__(self):
        return f'{self.room} | {self.customer}'

    def date_range(self):
        return f'{self.check_in} | {self.check_out}'

    def total_capacity(self):
        return 1 + self.capacity

    def check_payments(self):
        return True if self.payment_value > 0 else False

    def difference(self):
        return self.final_value - self.payment_value

    def calculate_days(self, checkOut=False):
        start_date, end_date = self.check_in, self.check_out
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        diff = end_date - start_date
        return diff.days

    def active_status(self):
        return False if self.isDone else False if self.isCancel else True

    def str_status(self):
        if not self.isDone and not self.isCancel:
            return 'ΣΕ ΕΞΕΛΙΞΗ' if self.checkIn else 'ΚΡΑΤΗΣΗ'
        return 'ΟΛΟΚΛΗΡΩΜΕΝΗ' if self.isDone and not self.isCancel else 'ΑΚΥΡΩΜΕΝΗ'

    def color_for_calendar(self):
        if self.isCancel:
            return 'yellow'
        if self.isDone:
            return 'red'
        if self.checkIn:
            return 'green'
        return 'teal'

    def tag_status(self):
        if self.checkIn and self.isDone:
            return 'ΟΛΟΚΛΗΡΩΜΕΝΟ'
        if self.isCancel:
            return 'ΑΚΥΡΩΜΕΝΟ'
        if self.checkIn and not self.isDone:
            return 'CHECK IN'
        if not self.checkIn and not self.isCancel:
            return 'ΑΝΑΜΟΝΗ'

    def current_charge(self):
        today = datetime.datetime.now().date()
        diff = today - self.check_in
        days = diff.days
        day_avg = self.final_value/self.days if self.days != 0 else 0
        if not self.checkIn:
            return 0
        if days == 0:
            return day_avg
        return (self.final_value/self.days)*days

    def create_extra_charges(self, capacity, days):
        for ele in self.room.my_extras.all():
            value = ele.value * capacity if ele.capacity else ele.value
            value = value * days if ele.day_charge else value
            ExtraCharge.objects.create(
                reservation=self,
                title=ele.title,
                value=value,
                charges=1
            )

    def get_edit_url(self):
        return reverse('reservations:update_reservation', kwargs={'pk': self.id})

    def get_payment_status_url(self):
        return reverse('reservations:close_and_pay_reservation', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('reservations:delete_reservation', kwargs={'pk': self.id})

    def calendar_color(self):
        if self.checkIn:
            return 'green'
        if self.isCancel:
            return 'red'
        if self.isDone:
            return 'blue'
        return 'white'

    def cancel_process(self):
        self.isCancel = True
        self.isDone = False
        self.checkIn = False
        self.save()

    def reservation_calculate_real_cost(self):
        extra_cost = (self.capacity - 1) * self.extra_cost_per_person
        day_cost = extra_cost + self.value
        days = self.calculate_days(checkOut=datetime.datetime.now().date())
        print('days!', days)
        return days * day_cost

    def calculate_current_days(self):
        return self.calculate_days(checkOut=datetime.datetime.now().date())

    def create_reservation(self):
        # this function is used for creating new reservation or transfer room
        # checks if we used our own prices and if not starts to calculate the prices
        # be careful is used on signals
        date_list, room, days = [], self.room, self.calculate_days()
        self.days = days
        self.create_extra_charges(self.capacity, days)
        if self.clean_value == 0:
            for i in range(days):
                create_date = self.check_in
                if isinstance(create_date, str):
                    create_date = datetime.datetime.strptime(create_date, '%Y-%m-%d')
                date = create_date + datetime.timedelta(days=i)
                date_list.append(date.strftime("%Y-%m-%d"))
            new_value = room.reservation_find_price(date_list, self.capacity-1)
            self.clean_value = new_value[0]
            self.extra_cost_per_person = new_value[1]
            self.save()
        room.used = True
        room.save()

    def close_reservation(self, movement):
        movements = ['payment', 'is_cancel']
        room = self.room
        if movement not in movements:
            return False
        if movement == 'payment':
            value = self.final_value - self.payment_value
            if value > 0:
                new_payment = CustomerPayment.objects.create(
                    customer=self.customer,
                    value=value,
                    date=datetime.datetime.now()
                )
            self.checkIn = False
            self.isCancel = False
            self.isDone = True
            self.check_out = datetime.datetime.now()
            self.save()

            room.used = False
            room.save()
        if movement == 'is_cancel':
            self.isCancel = True
            self.checkIn = False
            self.isDone = False
            self.value = self.payment_value
            self.extra_cost_per_person = 0
            self.save()

    @staticmethod
    def check_room_prices(request, qs):
        date_start, date_end, date_range = initial_date(request, 6)
        try:
            people = int(request.GET.get('people', 2))
        except:
            people = 1

        room_list = []
        for room in qs:
            is_available = room.check_availability(check_in=date_start, check_out=date_end)
            price = room.estimate_prices_for_search_filters(date_start, date_end, people)

            # price = room.search_price(date_start, date_end, people)
            room_list.append({
                'room': room,
                'is_available': is_available,
                'price': price
            })
        return room_list

    @staticmethod
    def filters_data(request, qs):
        room_name = request.GET.getlist('room_name', None)
        status_name = request.GET.getlist('status_name', None)
        customer_name = request.GET.getlist('customer_name', None)
        q = request.GET.get('search_name', None)
        date_start, date_end, date_range = initial_date(request, 6)

        qs = qs.filter(room__in=room_name) if room_name else qs
        if q:
            qs = qs.filter(Q(room__title__icontains=q) |
                           Q(customer__title__icontains=q)
                           )

        if date_start and date_end:
            second_guess_res = qs
            qs = qs.filter(check_in__lt=date_end)
            qs = qs.filter(check_out__gt=date_start)
            second_guess_res = second_guess_res.filter(check_in__gte=date_start)
            second_guess_res = second_guess_res.filter(check_out__lt=date_end)
            qs = qs | second_guess_res

        qs_1, qs_2, qs_3 = 3*[Reservation.objects.none()]
        if status_name:
            if 'active' in status_name:
                qs_1 = qs.filter(isDone=False, isCancel=False)
            if 'done' in status_name:
                qs_2 = qs.filter(isDone=True, isCancel=False)
            if 'cancel' in status_name:
                qs_3 = qs.filter(isCancel=True)
            qs = qs_1 | qs_2 | qs_3
        return qs


class ExtraCharge(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='extra_charges')
    title = models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='ΑΞΙΑ ΜΟΝΑΔΑΣ')
    charges = models.IntegerField(default=1, verbose_name='ΧΡΕΩΣΕΙΣ')
    final_value = models.DecimalField(default=0, max_digits=20, decimal_places=2, verbose_name='ΑΞΙΑ')

    def save(self, *args, **kwargs):
        self.final_value = self.value * self.charges
        super(ExtraCharge, self).save(*args, **kwargs)
        self.reservation.save()

    def __str__(self):
        return f'{self.reservation} | {self.title}'


    def create_charge(self, charge):
        pass