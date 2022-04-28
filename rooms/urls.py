from django.urls import path

from .views import (RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomCardView)
from .actions_views import (room_price_create_view, room_price_edit_view, room_price_delete_view,
                            action_add_remove_room_from_card_view, room_price_add_remove_price_view,
                            room_charge_add_remove_price_view, room_charge_create_view

                            )

from .price_views import (RoomPriceListView, RoomPriceCreateView, RoomPriceUpdateView, RoomPriceDeleteView,
                          room_price_card_view
                          )
from .room_charges_view import RoomChargeListView, RoomChargeUpdateView, RoomChargeCreateView, RoomChargeDeleteView, room_charge_card_view

app_name = 'rooms'

urlpatterns = [
    path('list/', RoomListView.as_view(), name='list'),
    path('create/', RoomCreateView.as_view(), name='create'),
    path('update/<int:pk>/', RoomUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', RoomDeleteView.as_view(), name='delete'),
    path('card/<int:pk>/', RoomCardView.as_view(), name='card'),

    # actions views
    path('action/create-price/<int:pk>/', room_price_create_view, name='action_room_price'),
    path('room-price/edit/<int:pk>/', room_price_edit_view, name='action_room_price_edit'),
    path('room-price/delete/<int:pk>/', room_price_delete_view, name='action_room_price_delete'),
    path('action-room-card-add-remove/<int:pk>/<int:dk>/<str:action>/',
         action_add_remove_room_from_card_view, name='action_room_price_card_add_remove'),

    path('action/room-add-remove-price/<int:pk>/<int:dk>/<str:action>/', room_price_add_remove_price_view,
         name='room_price_add_remove'),

    path('action/charge-price/<int:pk>/', room_charge_create_view, name='action_room_charge'),
    path('action/charge-add-remove-price/<int:pk>/<int:dk>/<str:action>/', room_charge_add_remove_price_view,
         name='room_charge_add_remove'),

    # room_views
    path('room-price/list/', RoomPriceListView.as_view(), name='room_price_list'),
    path('room-price/create/', RoomPriceCreateView.as_view(), name='room_price_create'),
    path('room-price/update/<int:pk>/', RoomPriceUpdateView.as_view(), name='room_price_update'),
    path('room-price/delete-S/<int:pk>/', RoomPriceDeleteView.as_view(), name='room_price_delete'),
    path('room-price-card/<int:pk>/', room_price_card_view, name='room_price_card'),


    # room values

    path('room-charge/list/', RoomChargeListView.as_view(), name='room_charge_list'),
    path('room-charge/create/', RoomChargeCreateView.as_view(), name='room_charge_create'),
    path('room-charge/update/<int:pk>/', RoomChargeUpdateView.as_view(), name='room_charge_update'),
    path('room-charge/delete-S/<int:pk>/', RoomChargeDeleteView.as_view(), name='room_charge_delete'),
    path('room-charge-card/<int:pk>/', room_charge_card_view, name='room_charge_card'),





]