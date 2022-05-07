from django.db import models
from datetime import datetime
from datetime import timedelta

from frontend.tools import initial_date


class ReservationManager(models.Manager):

    def active_or_waiting_arrive(self, request):
        qs = self.filter(isDone=False, isCancel=False)
        room_name = request.GET.getlist('room_name', None)
        date_start, date_end, date_range = initial_date(request, 1)
        qs = self.filter(room__id__in=room_name) if room_name else qs
        if date_start and date_end:
            print('date exsts', date_start, date_end)
            qs = qs.filter(check_in__gte=date_start, check_in__lt=date_end)
        return qs

    def rooms_with_people(self):
        return self.filter(isDone=False, isCancel=False, checkIn=True)

    def rooms_wait_people_arrive(self):
        return self.filter(isDone=False, isCancel=False, checkIn=False)

    def rooms_leaving_today(self):
        return self.rooms_with_people().filter(check_out=datetime.now())

    def check_for_reservations(self, request) -> list:
        reservations = self.active_or_waiting_arrive(request)
        used_rooms = reservations.values_list('room_id')
        return used_rooms

    def filters_data(self, request):
        room_name = request.GET.getlist('room_name', None)
        date_start, date_end, date_range = initial_date(request, 6)
        qs = self.all()
        qs = self.filter(room__id__in=room_name) if room_name else qs
        if date_start and date_end:
            qs = qs.filter(check_in__gte=date_start, check_in__lt=date_end)


        return qs
