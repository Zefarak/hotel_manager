import django_tables2 as tables

from .models import Reservation


class ReservationTable(tables.Table):
    button = tables.TemplateColumn("<a target='_blank' href='{{ record.get_edit_url }}' class='btn btn-info' ><i class='fa fa-edit'></i></a>",
                                   orderable=False, verbose_name='-'
                                   )
    str_status = tables.Column(orderable=False, verbose_name='ΚΑΤΑΣΤΑΣΗ')

    class Meta:
        model = Reservation
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date_range', 'room', 'customer', 'str_status', 'final_value',]
