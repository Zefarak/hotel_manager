from django.db import models


class RoomManager(models.Manager):

    def active(self):
        return self.filter(active=True)

