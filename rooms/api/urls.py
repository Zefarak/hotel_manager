from django.urls import path

from .views import RoomListCreateApiView, RoomPriceListCreateApiView, room_homepage_view

app_name = 'api_rooms'

urlpatterns = [
    path('', room_homepage_view, name='home'),
    path('rooms/', RoomListCreateApiView.as_view(), name='rooms'),
    path('rooms-price/', RoomPriceListCreateApiView.as_view(), name='rooms-price')
]