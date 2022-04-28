from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q, Sum
from django.shortcuts import render

import datetime

from reservations.models import Reservation, Customer
from customers.models import CustomerPayment
from payroll.models import Bill
from .models import PaymentMethod


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['rooms_leaving'] = Reservation.my_query.rooms_leaving_today()
        context['rooms_arrive'] = Reservation.my_query.rooms_wait_people_arrive()
        context['room_in_progress'] = Reservation.my_query.rooms_with_people()
        payment_qs = CustomerPayment.objects.filter(date__month=datetime.datetime.now().month)
        reserv_qs = Reservation.objects.filter(check_in__month=datetime.datetime.now().month, isCancel=False) # Reservation.objects.filter(check_in__range=[datetime.datetime.now().replace(day=1), datetime.datetime.now().replace(day=30)],isCancel=False)

        context['monthly_incomes'] = payment_qs.aggregate(Sum('value'))['value__sum'] if payment_qs.exists() else 0
        context['monthly_reserv'] = reserv_qs.aggregate(Sum('final_value'))['final_value__sum'] if reserv_qs.exists() else 0
        context['bills'] = Bill.objects.filter(is_paid=False).aggregate(Sum('final_value'))['final_value__sum'] if Bill.objects.filter(is_paid=False).exists() else 0
        return context



def change_name_view(request):
    qs = Customer.objects.all()
    print('here')
    for ele in qs:
        title = ele.title
        split = title.split(' ')
        new_title = f'{split[-1]}'
        for i in split[:-1]:
            new_title = new_title + f' {i}'
        ele.title = new_title
        ele.save()
        print('new title', new_title)
    return render(request, 'dashboard.html')