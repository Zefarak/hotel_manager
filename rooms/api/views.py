from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .serializers import RoomPriceSerializer, RoomSerializer
from ..models import RoomPrice, Room



@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def room_homepage_view(request, format=None):
    return Response({
        'rooms': reverse('api_rooms:rooms', request=request, format=format),
        'rooms_price': reverse('api_rooms:rooms-price', request=request, format=format)
    })


class RoomListCreateApiView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class RoomPriceListCreateApiView(generics.ListCreateAPIView):
    queryset = RoomPrice.objects.all()
    serializer_class = RoomPriceSerializer
