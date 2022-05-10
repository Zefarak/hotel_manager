from rest_framework import serializers

from ..models import Room, RoomCharge, RoomPrice


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'title', 'active', 'used', 'notes', 'value', 'capacity', 'extra_value_per_person']


class RoomPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomPrice
        fields = ['id', 'title', 'active', 'room', 'minimum_days',
                  'date_start', 'date_end', 'value', 'extra_value_per_person', 'price'
                  ]