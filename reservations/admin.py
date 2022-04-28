from django.contrib import admin

# Register your models here.

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass