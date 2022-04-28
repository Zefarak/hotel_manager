from django.test import TestCase


from customers.models import Customer, CustomerPayment
from rooms.models import Room, RoomPrice, RoomCharge
from .models import Reservation


import datetime


class TestFlowCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(title='Customer 1')
        self.room = Room.objects.create(title='Room 1', value=100, extra_value_per_person=50, capacity=2)
        self.room_1 = Room.objects.create(title='102', value=100, extra_value_per_person=10, capacity=2)
        self.room_2 = Room.objects.create(title='201', value=100, extra_value_per_person=30, capacity=4)
        self.room_price_1 = RoomPrice.objects.create(title='Christmas', date_start='2021-12-1', date_end='2021-12-30',
                                                     value=180, extra_value_per_person=20
                                                     )
        self.extra_1 = RoomCharge.objects.create(title='Breakfast_1', value=10, capacity=True, day_charge=True)
        self.customer = Customer.objects.create(title='Stathakis')

    def test_room_prices(self):
        self.room_price_1.room.add(self.room)
        self.room_price_1.save()
        new_reservation = Reservation.objects.create(
            room=self.room,
            check_in='2021-12-1',
            check_out='2021-12-2',
            customer=self.customer,
            capacity=1
        )

        self.assertEqual(new_reservation.final_value, 360)

        second_reservation = Reservation.objects.create(
            room=self.room,
            check_in='2021-11-30',
            check_out='2021-12-2',
            customer=self.customer,
            capacity=1
        )

        self.assertEqual(second_reservation.final_value, 460)

    def test_reservation_creation(self):
        self.extra_1.room.add(self.room)
        self.extra_1.save()
        obj = Reservation.objects.create(
            room=self.room,
            check_in='2021-12-1',
            check_out='2021-12-3',
            customer=self.customer,
            capacity=2,
            clean_value=50
        )
        for room in obj.extra_charges.all():
            print(room.tag_final_value)
        self.assertEqual(obj.value, 50)
        self.assertEqual(obj.extra_charges.count(), 1)
        # self.assertEqual(obj.charges_value, 40)




