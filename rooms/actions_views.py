from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


from .models import Room, RoomPrice, RoomCharge
from .forms import RoomPriceForm


@staff_member_required
def room_price_create_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    prices = RoomPrice.objects.all()
    page_title, back_url = f'ΠΡΟΣΘ/ΑΦΑΙΡ ΤΙΜΩΝ ΑΠΟ ΔΩΜΑΤΙΟ {room}',  room.get_card_url()
    return render(request, 'room/add_remove_prices_from_card.html', locals())


@staff_member_required
def room_price_add_remove_price_view(request, pk, dk, action):
    room = get_object_or_404(Room, id=pk)
    price = get_object_or_404(RoomPrice, id=dk)
    if action == 'add':
        price.room.add(room)
    if action == 'remove':
        price.room.remove(room)
    price.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def room_charge_create_view(request, pk):
    room = get_object_or_404(Room, id=pk)
    charges = RoomCharge.objects.all()
    page_title, back_url = f'ΠΡΟΣΘ/ΑΦΑΙΡ ΧΡΕΩΣΕΩΝ ΑΠΟ ΔΩΜΑΤΙΟ {room}',  room.get_card_url()
    return render(request, 'room/extra_charges_view.html', locals())


@staff_member_required
def room_charge_add_remove_price_view(request, pk, dk, action):
    room = get_object_or_404(Room, id=pk)
    charge = get_object_or_404(RoomCharge, id=dk)
    if action == 'add':
        charge.room.add(room)
    if action == 'remove':
        charge.room.remove(room)
    charge.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def room_price_edit_view(request, pk):
    obj = get_object_or_404(RoomPrice, id=pk)
    form = RoomPriceForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Η ΤΙΜΗ ΔΗΜΙΟΥΡΓΗΘΗΚΕ')
        return redirect(obj.room.get_card_url())
    delete_url, back_url = obj.get_delete_url(), obj.room.get_card_url()
    return render(request, 'generic_templates/form.html', context=locals())


@staff_member_required
def room_price_delete_view(request, pk):
    obj = get_object_or_404(RoomPrice, id=pk)
    obj.delete()
    return obj.room.get_card_url()


@staff_member_required
def action_add_remove_room_from_card_view(request, pk, dk, action):
    price = get_object_or_404(RoomPrice, id=pk)
    room = get_object_or_404(Room, id=dk)
    if action == 'add':
        price.room.add(room)
    if action == 'delete':
        price.room.delete(room)
    price.save()
    return redirect(price.get_card_url())
