from django.contrib import admin

from .models import Customer, CustomerPayment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerPayment)
class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'value']
