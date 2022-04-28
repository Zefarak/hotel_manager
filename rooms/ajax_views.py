from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from rooms.models import Room


@staff_member_required
def ajax_prices_modal_view(request, pk):
    print('hitted')
    room = get_object_or_404(Room, id=pk)
    prices = room.extra_prices.all()
    content = dict()
    content['result'] = render_to_string(
        template_name='reservations/ajax/room_price_modal.html',
        request=request,
        context=locals()
    )
    return JsonResponse(content)
