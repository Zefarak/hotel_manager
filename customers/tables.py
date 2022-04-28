import django_tables2 as tables

from .models import Customer, CustomerPayment


class CustomerTable(tables.Table):
    button = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-info' ><i class='fa fa-edit'></i></a>",
                                   orderable=False, verbose_name='-'
                                   )
    card = tables.TemplateColumn("<a href='{{ record.get_card_url }}' class='btn btn-primary' ><i class='fa fa-eye'></i></a>",
                                   orderable=False, verbose_name='card'
                                   )

    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'phone', 'country', 'balance', 'button', 'card']


class PaymentTable(tables.Table):

    class Meta:
        model = CustomerPayment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'payment_type', 'value']
