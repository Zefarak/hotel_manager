from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .models import Reservation, ExtraCharge, CustomerPayment
import datetime


@receiver(post_save, sender=Reservation)
def calculate_price(sender, instance, created, **kwargs):
    if created:
        instance.create_reservation()
        '''
        date_list, room, days = [], instance.room, instance.calculate_days()
        instance.days = instance.calculate_days()
        if instance.value == 0:
            # create list of days
            for i in range(days):
                create_date = instance.check_in
                date = create_date + datetime.timedelta(days=i)
                date_list.append(date.strftime("%Y-%m-%d"))
            """
            for i in range(days):
                create_date = datetime.datetime.strptime(instance.check_in, "%Y-%m-%d")
                date = create_date + datetime.timedelta(days=i)
                date_list.append(date.date().strftime("%Y-%m-%d"))
            """
            new_value = room.reservation_find_price(date_list, instance.capacity-1)
            instance.clean_value = new_value[0]
            instance.extra_cost_per_person = new_value[1]
            instance.save()
            room.used = True
            room.save()
        '''


@receiver(post_save, sender=Reservation)
def update_status_on_reservations(sender, instance, *args, **kwargs):
    if instance.isCancel and instance.checkIn:
        instance.checkIn = False
        instance.isDone = False
        instance.save()

    if instance.isDone and not instance.checkIn:
        instance.checkIn = True
        instance.isCancel = False
        instance.save()


@receiver(post_delete, sender=Reservation)
def update_room_and_customer_on_delete(sender, instance, **kwargs):
    if instance.room:
        room = instance.room
        room.save()
    if instance.customer:
        customer = instance.customer
        customer.save()


@receiver(post_delete, sender=ExtraCharge)
def update_reservation_after_delete(sender, instance, **kwargs):
    instance.reservation.save()


@receiver(post_delete, sender=CustomerPayment)
def update_payment_after_delete(sender, instance, **kwargs):
    if instance.reservation:
        instance.reservation.save()
    if instance.customer:
        instance.customer.save()