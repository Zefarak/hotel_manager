from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

import datetime

from .manager import RoomManager
from .tools import initial_date


def find_free_rooms(request, qs):
    print('hey')
    date_start, date_end, date_range = initial_date(request, 3)
    final_qs = qs
    ids = []
    for room in qs:
        print(room, room.title, room.id)
        res = room.bookings.filter(isDone=False, isCancel=False)
        second_guess_res = room.bookings.all()
        res = res.filter(check_in__lt=date_end)
        print('first guess', res)
        res = res.filter(check_out__gt=date_start)
        print('second', res)
        if res.exists():
            ids.append(room.id)
        else:
            second_guess_res = second_guess_res.filter(check_in__gte=date_start)
            print('third', second_guess_res)
            second_guess_res = second_guess_res.filter(check_out__lt=date_end)
            print('four', second_guess_res)
            if second_guess_res.exists():
                ids.append(room.id)
    return final_qs.exclude(id__in=ids)


class Room(models.Model):
    active = models.BooleanField(default=True, verbose_name='ΚΑΤΑΣΤΑΣΗ')
    used = models.BooleanField(default=False, verbose_name='ΧΡΗΣΙΜΟΠΟΙΕΙΤΑΙ')
    title = models.CharField(max_length=200, unique=True, verbose_name='ΤΙΤΛΟΣ')
    notes = HTMLField(blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΒΑΣΙΚΗ ΤΙΜΗ')
    extra_value_per_person = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΕΠΙΠΛΕΟΝ ΚΟΣΤΟΣ ΑΝΑ ΑΤΟΜΟ')
    capacity = models.IntegerField(default=2, verbose_name='ΜΕΓΙΣΤΗ ΧΩΡΗΤΙΚΟΤΗΤΑ')
    extra_charges = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΕΠΙΠΛΕΟΝ ΤΙΜΗ', default=0)
    my_query = RoomManager()
    objects = models.Manager()

    class Meta:
        ordering = ['title', ]

    def save(self, *args, **kwargs):
        checkIn = self.bookings.filter(checkIn=True, isDone=False, isCancel=False).exists()
        self.used = checkIn
        if self.id:
            extra_qs = self.my_extras.all()
            if extra_qs.exists():
                self.extra_charges = self.calculate_extras()
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def calculate_extras(self):
        sum = 0
        for ele in self.my_extras.all():
            value = ele.value*self.capacity if ele.capacity else ele.value
            sum += value
        return sum

    def tag_final_price(self, capacity, date_start, date_end):
        value = self.search_price(date_start, date_end, capacity-1)
        extras = self.calculate_extras()
        return value[0] + value[1] + extras

    def get_current_reservation(self):
        qs = self.bookings.filter(checkIn=True, isDone=False, isCancel=False)
        return qs.last() if qs.exists() else None

    def calculate_price(self, capacity):
        return self.value + (capacity*self.extra_value_per_person)

    def search_price(self, date_start, date_end, extra_people):

        if not date_start or not date_end:
            return [0, 0]
        qs = self.extra_prices.filter(
            date_start__lte=date_start,
            date_end__gte=date_start
          )
        return qs.first().get_price(extra_people) if qs.exists() else \
            [self.value, self.extra_value_per_person*extra_people]

    def estimate_prices_for_search_filters(self, date_start, date_end, extra_people):
        price_per_day, extra_prices = self.search_price(date_start, date_end, extra_people-1)
        summary_extras = 0
        days = (date_end - date_start).days
        for extra in self.my_extras.all():
            if extra.day_charge:
                value = extra.value * days if extra.day_charge else extra.value
                value = value * extra_people if extra.capacity else value
                summary_extras += value
        return [price_per_day, extra_prices, summary_extras]

    def reservation_find_price(self, days: list, extra_people=0) -> list:
        final_price, size = [0, 0],  len(days)  # [value, extra_cost_per_person]

        for i in range(size):
            day = days[i]
            value = self.search_price(day, day, extra_people)
            final_price[0] += value[0]
            final_price[1] += value[1]
        return final_price

    def get_edit_url(self):
        return reverse('rooms:update', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('rooms:card', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('rooms:delete', kwargs={'pk': self.id})

    def get_action_create_reservation_url(self):
        return reverse('reservations:action-create-reservation', kwargs={'pk': self.id})

    def check_availability(self, check_in, check_out):
        if type(check_in) == str:
            check_in = datetime.datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out = datetime.datetime.strptime(check_out, '%Y-%m-%d').date()
        bookings = self.bookings.all()
        avail_list = []
        check_out = datetime.datetime.combine(check_out,  datetime.time(0, 0))
        check_in = datetime.datetime.combine(check_in, datetime.time(0, 0))
        for booking in bookings:
            if datetime.datetime.combine(booking.check_in, datetime.time(0, 0)) > check_out or datetime.datetime.combine(booking.check_out, datetime.time(0, 0)) < check_in:
                avail_list.append(True)
            else:
                return False
        return True

    @staticmethod
    def filter_qs(request, qs):
        people = request.GET.get('people')
        try:
            people = int(people)
            qs = qs.filter(capacity__gte=people)
        except:
            people = 2
        qs = find_free_rooms(request, qs)
        return qs


class RoomPrice(models.Model):
    title = models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')
    active = models.BooleanField(default=True, verbose_name='ΚΑΤΑΣΤΑΣΗ')
    room = models.ManyToManyField(Room,  verbose_name='ΔΩΜΑΤΙΟ', related_name='extra_prices', blank=True, null=True)

    minimum_days = models.IntegerField(default=0, verbose_name='ΕΛΑΧΙΣΤΕΣ ΜΕΡΕΣ')
    date_start = models.DateField()
    date_end = models.DateField()

    value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='ΑΞΙΑ')
    extra_value_per_person = models.DecimalField(decimal_places=2, max_digits=20,
                                                 default=0, verbose_name='ΕΠΙΠΛΕΟΝ ΑΞΙΑ ΑΝΑ ΑΤΟΜΟ')
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2, verbose_name='ΤΙΜΗ ΔΩΜΑΤΙΟΥ')

    class Meta:
        ordering = ['date_start']
    
    def save(self, *args, **kwargs):
        self.price = self.value
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def calculate_price(self, extra_person):
        return self.price + (extra_person*self.extra_value_per_person)

    def date_range(self):
        return f'{self.date_start} | {self.date_end}'

    def get_price(self, extra_people):
        value = self.price
        extra = self.extra_value_per_person * extra_people

        return [value, extra]

    def get_edit_url(self):
        return reverse('rooms:action_room_price_edit', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('rooms:room_price_update', kwargs={'pk': self.id})

    def get__delete_url(self):
        return reverse('rooms:room_price_delete', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('rooms:room_price_card', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('rooms:action_room_price_delete', kwargs={'pk': self.id})


class RoomCharge(models.Model):
    capacity = models.BooleanField(default=False, verbose_name='ΧΡΕΩΣΗ ΑΝΑ ΑΤΟΜΟ')
    day_charge = models.BooleanField(default=False, verbose_name='ΧΡΕΩΣΗ ΑΝΑ ΗΜΕΡΑ')
    title = models.CharField(unique=True, max_length=230, verbose_name='ΤΙΤΛΟΣ')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='ΑΞΙΑ')
    room = models.ManyToManyField(Room, verbose_name='ΔΩΜΑΤΙΑ', blank=True, null=True, related_name='my_extras')

    def __str__(self):
        return self.title

    def calculate_value(self, capacity, days=1):
        sum = self.value
        if self.capacity:
            sum = self.value * capacity
        if self.day_charge:
            sum = sum * days
        return sum

    def get_update_url(self):
        return reverse('rooms:room_charge_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('rooms:room_charge_delete', kwargs={'pk': self.id})

    def get_card_url(self):
        return reverse('rooms:room_charge_card', kwargs={'pk': self.id})


