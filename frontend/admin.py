from django.contrib import admin

# Register your models here.
from .models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass