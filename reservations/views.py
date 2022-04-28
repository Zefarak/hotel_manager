from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages

import datetime
from django_tables2 import RequestConfig

from rooms.models import Room
from customers.forms import CustomerForm
from .models import Reservation, Customer
from .tables import ReservationTable
from .forms import ReservationForm, ExtraChargeForm, ReservationUpdateForm, ReservationCreateForm
from customers.forms import CustomerPaymentForm

from .tools import find_free_rooms_helper


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'reservations/reservations.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['date_filter'] = True
        rooms = Room.objects.filter(active=True)
        if self.request.GET.get('search_exist'):
            rooms = Room.filter_qs(self.request, Room.objects.filter(active=True))
        check_in, check_out = [self.request.GET.get('check_in'),
                               self.request.GET.get('check_out')
                               ]

        all_rooms = [{'room': room} for room in rooms]
        context['reservations'] = Reservation.my_query.active_or_waiting_arrive(self.request).order_by('check_in', 'checkIn')
        context['all_rooms'] = all_rooms
        if self.request.GET.get('date_range', False):
            context['all_rooms'] = Reservation.check_room_prices(self.request, rooms)
        context['rooms'] = rooms
        context['qs_data'] = Reservation.objects.all()

        # timeline calendar. what to do what to do
        available_rooms = Room.objects.filter(active=True)
        rooms_list = []
        for room in available_rooms:
            room = {'id': room.id, "title": room.title}
            rooms_list.append(room)
        context['room_list'] = rooms_list
        rooms_availability = []
        for room in rooms:
            if check_in and check_out:
                if room.check_availability(check_in, check_out):
                    rooms_availability.append(room)
            else:
                rooms_availability.append(room)
        context['rooms_availability'] = rooms_availability
        return context


@method_decorator(staff_member_required, name='dispatch')
class ReservationListView(ListView):
    template_name = 'generic_templates/list.html'
    model = Reservation
    paginate_by = 100
    
    def get_queryset(self):
        qs = self.model.filters_data(self.request, Reservation.objects.all())
        return qs

    def get_context_data(self,  **kwargs):
        context = super(ReservationListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Reservations'
        qs_table = ReservationTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        context['customers'] = Customer.objects.all()
        context['rooms'] = Room.objects.all()
        context['room_filter'], context['customer_filter'], context['search_filter'] = [True]*3
        context['cancel_done_filter'] = True
        context['queryset_table'] = qs_table

        return context


@method_decorator(staff_member_required, name='dispatch')
class ReservationCreateView(CreateView):
    template_name = 'generic_templates/form.html'
    model = Reservation
    form_class = ReservationCreateForm
    success_url = reverse_lazy('reservations:homepage')

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ RESERVATION'
        context['back_url'] = self.success_url
        context['extra_form'] = CustomerForm()
        context['extra'] = True
        return context

    def form_valid(self, form):
        reservation = form.save()
        advance = form.cleaned_data.get('advance', False)
        if advance:
            self.success_url = reverse('reservations:create-payment-reservation', kwargs={'pk': reservation.id})
        return super(ReservationCreateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ReservationUpdateView(UpdateView):
    template_name = 'reservations/reservation_update_view.html'
    model = Reservation
    form_class = ReservationUpdateForm
    success_url = reverse_lazy('reservations:homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΕΠΕΞΕΡΓΑΣΙΑ {self.object}'
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        context['rooms'] = Room.objects.filter(used=False)
        context['extra_form'] = ExtraChargeForm(self.request.POST or None, initial={'reservation': self.object,})
        context['payment_form'] = CustomerPaymentForm(self.request.POST or None, initial={'reservation': self.object,
                                                                                          'customer': self.object.customer
                                                                                          })
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Οι αλλαγές αποθηκεύτηκαν με επιτυχία.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ReservationDeleteView(DeleteView):
    template_name = 'form_view.html'
    model = Reservation
    success_url = reverse_lazy('reservations:homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'ΔΙΑΓΑΦΗ'
        context['back_url'] = self.object.get_edit_url()
        return context


@staff_member_required
def close_reservation_and_pay_view(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    if reservation.isCancel or not reservation.checkIn:
        messages.error(request, 'Η ΚΡΑΤΗΣΗ ΕΧΕΙ ΑΚΥΡΩΘΕΙ Η ΔΕ ΕΧΕΙ ΕΡΘΕΙ')
    costumer_form = CustomerPaymentForm(request.POST or None, initial={
                                        'customer': reservation.customer,
                                        'reservation': reservation,
                                        'value': reservation.final_value-reservation.payment_value,
                                        'date': datetime.datetime.now().today()
        }
    )
    if costumer_form.is_valid():
        pay = costumer_form.cleaned_data.get('value')
        if pay > 0:
            new_payment = costumer_form.save()
        reservation.isDone = True
        reservation.save()

        messages.success(request, 'Η διαμονη ολοκληρώθηκε.')
        return redirect(reverse('reservations:homepage'))

    return render(request,
                  'reservations/reservation_close_and_pay.html',
                  context={
                      'reservation': reservation,
                      'payment_form': costumer_form
                  }
                  )


@staff_member_required
def print_reservation_view(request, pk):
    instance = get_object_or_404(Reservation, id=pk)

    return render(request, 'print/index.html', context=locals())