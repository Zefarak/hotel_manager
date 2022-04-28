from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import CustomerPayment


@receiver(post_delete, sender=CustomerPayment)
def update_balance_to_customer(sender, instance, **kwargs):
    instance.customer.save()
    if instance.reservation:
        instance.reservation.save()