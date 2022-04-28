import django_tables2 as tables

from .models import Room, RoomPrice, RoomCharge


class RoomTable(tables.Table):
    button = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-info' ><i class='fa fa-edit'></i></a>",
                                   orderable=False, verbose_name='-'
                                   )
    card = tables.TemplateColumn("<a href='{{ record.get_card_url }}' class='btn btn-info' ><i class='fa fa-eye'></i></a>",
                                   orderable=False, verbose_name='-'
                                   )

    class Meta:
        model = Room
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title',  'capacity', 'value', 'notes', 'active', 'used' ]


class RoomPriceTable(tables.Table):
    button = tables.TemplateColumn(
        "<a href='{{ record.get_update_url }}' class='btn btn-info' ><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='-'
        )
    card = tables.TemplateColumn(
        "<a href='{{ record.get_card_url }}' class='btn btn-info' ><i class='fa fa-eye'></i></a>",
        orderable=False, verbose_name='ΚΑΡΤΕΛΑ'
    )

    class Meta:
        model = RoomPrice
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'date_range', 'price']


class RoomChargeTable(tables.Table):
    button = tables.TemplateColumn(
        "<a href='{{ record.get_update_url }}' class='btn btn-info' ><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='-'
        )
    card = tables.TemplateColumn(
        "<a href='{{ record.get_card_url }}' class='btn btn-info' ><i class='fa fa-eye'></i></a>",
        orderable=False, verbose_name='ΚΑΡΤΕΛΑ'
    )

    class Meta:
        model = RoomCharge
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', ]