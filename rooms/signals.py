from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Room