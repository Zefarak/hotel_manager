from django.urls import path

from .views import (HomepageView, ReservationListView, ReservationCreateView, ReservationUpdateView,
                    close_reservation_and_pay_view, ReservationDeleteView

                    )

from .action_views import (create_room_reservation_view, validate_customer_view, reservation_actions_view,
                           reservation_action_pay_view, recalculate_prices_view, action_remove_price_from_reservation,
                           change_room_and_check_availability_view, action_create_charge_from_reservarion,
                           create_new_payment_for_reservation_view, validate_create_or_delete_payment_for_reservation_view,
                           update_payment_view

                           )
from rooms.ajax_views import ajax_prices_modal_view

from .autocomplete_forms import CustomerAutocomplete

app_name = 'reservations'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),

    path('create-reservation/', ReservationCreateView.as_view(), name='create_reservation'),
    path('reservation-list/', ReservationListView.as_view(), name='reservation_list'),
    path('update-reservation/<int:pk>/', ReservationUpdateView.as_view(), name='update_reservation'),
    path('close-and-pay-reservation/<int:pk>/', close_reservation_and_pay_view, name='close_and_pay_reservation'),
    path('actions/reservation-pay/<int:pk>/<slug:movement>/', reservation_action_pay_view, name='action_reservation_pay'),
    path('delete-reservation/<int:pk>/', ReservationDeleteView.as_view(), name='delete_reservation'),


    # action
    path('action/create-room/<int:pk>/', create_room_reservation_view, name='action-create-reservation'),
    path('action/validate-customer-form/', validate_customer_view, name='validate_customer'),
    path('action/validate-customer-form/', validate_customer_view, name='validate_customer'),
    path('action/reservation-quick-action/<int:pk>/<slug:slug>/', reservation_actions_view, name='reservation_actions'),
    path('action/re-calculate-prices/<int:pk>/', recalculate_prices_view, name='recalculate_prices'),
    path('action/add-remove-extra-prices/<int:pk>/<int:dk>/', action_remove_price_from_reservation, name='remove_extra_prices'),
    path('action/change-room-on-reservation/<int:pk>/<int:dk>/<str:price>/', change_room_and_check_availability_view, name='change_room_prices'),
    path('action/create-charge-from-reservation/<int:pk>/', action_create_charge_from_reservarion, name='action_charge_from_reservation'),
    path('action/create-payment-from-reservation/<int:pk>/', create_new_payment_for_reservation_view, name='create-payment-reservation'),
    path('action/update-payment-reservation/<int:pk>/<slug:action>/', validate_create_or_delete_payment_for_reservation_view, name='update-delete-payment-reservation'),
    path('actions/update-payment/<int:pk>/', update_payment_view, name='update-payment'),



    path('autocomplete/find-customer/', CustomerAutocomplete.as_view(), name='auto_customers'),

    path('ajax/price-modal/<int:pk>/', ajax_prices_modal_view, name='ajax_room_price_modal'),
]