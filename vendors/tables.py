import django_tables2 as tables

from .models import Invoice, Payment, Vendor
# from products.models import Product





class VendorTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url}}' class='btn btn-warning'><span class='fa fa-edit'></span></a>", 
            orderable=False, verbose_name='-')
    tag_balance = tables.Column(orderable=False, verbose_name='Υπολοιπο')
    title =  tables.TemplateColumn("<a href='{{ record.get_edit_url}}'>{{ record }}</a>", 
            orderable=False, verbose_name='-')

    class Meta:
        model = Vendor
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'afm', 'phone',  'email', 'tag_balance']





    