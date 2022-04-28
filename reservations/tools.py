from .models import Room, Reservation


def find_free_rooms_helper(request):
    rooms = Room.objects.filter(active=True)
    reservations = Reservation.my_query.filters_data(request)
    used_rooms = []
    for reservation in reservations:
        used_rooms.append(reservation.room.id)
    rooms = rooms.exclude(id__in=used_rooms)
    return rooms
