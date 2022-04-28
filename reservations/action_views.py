from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import reverse

from .models import Reservation, Room, ExtraCharge
from .forms import ReservationForm, ExtraChargeForm
from customers.forms import CustomerPaymentForm

from customers.models import CustomerPayment
from customers.forms import CustomerForm, CustomerPaymentForm

import datetime


@staff_member_required
def validate_customer_view(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        new_obj = form.save()
        messages.success(request, f'Ο  πελάτης {new_obj.title} δημιουργήθηκε.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def create_room_reservation_view(request, pk):
    context = dict()
    context['obj'] = obj = get_object_or_404(Room, id=pk)
    context['reservations'] = obj.bookings.all() if obj.bookings.exists() else obj.bookings.none()
    context['extra_prices'] = obj.extra_prices.all()
    form = ReservationForm(request.POST or None, initial={'room': obj,
                                                          'clean_value': 0,
                                                          'extra_cost_per_person': 0
                                                        })
    if form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        is_available = True # obj.check_availability(check_in, check_out)
        if is_available:
            instance = form.save()
            instance.create_extra_charges(instance.capacity, instance.days)
            instance.save()
            return redirect('reservations:homepage')
        else:
            print('invalid dates!')
            messages.success(request, 'Invalid dates')
            return redirect(obj.get_action_create_reservation_url())
    else:
        print(form.errors)
    context['form'] = form
    context['customer_form'] = CustomerForm()
    context['room_price'] = obj.search_price(date_start=request.GET.get('date_start', datetime.datetime.today()),
                                             date_end=request.GET.get('date_end', datetime.datetime.today()),
                                             extra_people=0
                                             )
    context['final_value'] = obj.tag_final_price(capacity=1,
                                                 date_start=request.GET.get('date_start', datetime.datetime.today()),
                                                 date_end=request.GET.get('date_end', datetime.datetime.today()),
                                                 )
    return render(request, 'reservations/actions/create_reservation.html', context)


@staff_member_required
def reservation_actions_view(request, pk, slug):
    obj = get_object_or_404(Reservation, id=pk)
    choices = ['isCheck', 'isCancel', 'isDone']
    if not slug in choices:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if slug == 'isCheck':
        obj.checkIn = True
        obj.save()
    elif slug == 'isCancel':
        print('here')
        obj.cancel_process()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def reservation_action_pay_view(request, pk, movement):
    obj = get_object_or_404(Reservation, id=pk)
    movements = ['cancel', 'payment', 'edit']
    if movement not in movements:
        messages.error(request, 'Error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if movement == 'payment':
        obj.close_reservation(movement)
    if movement == 'cancel':
        obj.checkIn= False
        obj.isCancel = True
        obj.isDone = True
        obj.save()
    return redirect(reverse('reservations:homepage'))


@staff_member_required
def change_room_and_check_availability_view(request, pk, dk, price):
    reservation = get_object_or_404(Reservation, id=pk)
    new_room = get_object_or_404(Room, id=dk)
    old_room = reservation.room
    prices = ['room_price', 'reservation_price']
    check_in, check_out = reservation.check_in, reservation.check_out
    check_if_room_used = new_room.check_availability(check_in, check_out)
    if not check_if_room_used:
        messages.warning(request, 'ΤΟ ΔΩΜΑΤΙΟ ΕΧΕΙ ΚΡΑΤΗΣΗ ΤΗΝ ΣΥΓΚΕΚΡΙΜΕΝΗ ΠΕΡΙΟΔΟ')
        return redirect(reservation.get_edit_url())
    if price not in prices:
        return redirect(reservation.get_edit_url())

    if price == prices[0]:
        reservation.room = new_room
    if price == prices[1]:
        reservation.room = new_room
        reservation.create_reservation()
    reservation.save()
    old_room.save()
    return redirect(reservation.get_edit_url())


@staff_member_required
def recalculate_prices_view(request, pk):
    instance = get_object_or_404(Reservation, id=pk)
    date_list, room, days = [], instance.room, instance.calculate_days()
    instance.days = instance.calculate_days()
    for i in range(days):
        create_date = instance.check_in
        date = create_date + datetime.timedelta(days=i)
        date_list.append(date.strftime("%Y-%m-%d"))
        new_value = room.reservation_find_price(date_list, instance.capacity - 1)

        instance.value = new_value[0]
        instance.extra_cost_per_person = new_value[1]
    instance.save()
    if instance.checkIn:
        room.used = True
    room.save()
    instance.customer.save()
    return redirect(instance.get_edit_url())


@staff_member_required
def action_remove_price_from_reservation(request, pk, dk):
    reservation = get_object_or_404(Reservation, id=pk)
    price = get_object_or_404(ExtraCharge, id=dk)
    price.delete()
    return redirect(reservation.get_edit_url())


@staff_member_required
def action_create_charge_from_reservarion(request, pk):
    instance = get_object_or_404(Reservation, id=pk)
    form = ExtraChargeForm(request.POST or None, initial={'reservation': instance})
    if form.is_valid():
        form.save()
        messages.success(request, 'ΝΕΑ ΧΡΕΩΣΗ ΔΗΜΙΟΥΡΓΗΘΗΚΕ')
    else:
        print('error 66')
        messages.warning(request, form.errors)
    return redirect(instance.get_edit_url())


@staff_member_required
def create_new_payment_for_reservation_view(request, pk):
    instance = get_object_or_404(Reservation, id=pk)
    form = CustomerPaymentForm(request.POST or None,
                               initial={
                                   'reservation': instance,
                                   'customer': instance.customer,
                                   'value': instance.value/4

                               }

                               )
    if form.is_valid():
        form.save()
        messages.success(request, 'Η πληρωμή προστέθηκε')
        return redirect(reverse('reservations:homepage'))
    return render(request, 'form_view.html', context={
        'form': form,
        'back_url': reverse('reservations:homepage'),
        'page_title': f'Πληρωμή {instance}'
    })


@staff_member_required
def validate_create_or_delete_payment_for_reservation_view(request, pk, action):
    if action == 'update':
        instance = get_object_or_404(CustomerPayment, id=pk)
        form = CustomerPaymentForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
        else:
            messages.warning(request, 'Something is wrong')
    if action == 'create':
        instance = get_object_or_404(Reservation, id=pk)
        form = CustomerPaymentForm(request.POST or None, initial={'reservation': instance, 'customer': instance.customer})
        if form.is_valid():
            form.save()
        else:
            messages.warning(request, 'Something is wrong')
    if action == 'delete':
        instance = get_object_or_404(CustomerPayment, id=pk)
        instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def update_payment_view(request, pk):
    instance = get_object_or_404(CustomerPayment, id=pk)
    res = instance.reservation
    form = CustomerPaymentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse(reverse('reservations:update_reservation', kwargs={'pk': res.id})))
    else:
        messages.warning(request, 'Something is wrong')
    back_url = reverse('reservations:update_reservation', kwargs={'pk': res.id})
    page_title = f'ΕΠΕΞΕΡΓΑΣΙΑ ΠΛΗΡΩΜΗ {res}'
    return render(request, 'form_view.html', context=locals())
