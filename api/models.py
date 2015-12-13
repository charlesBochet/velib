from django.db import models


class Station(models.Model):
    number = models.PositiveIntegerField()
    contract_name = models.CharField(max_length=15)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()
    banking = models.BooleanField()
    bonus = models.BooleanField()
    status = models.CharField(max_length=6)
    bike_stands = models.PositiveSmallIntegerField(default=0)
    available_bike_stands = models.PositiveSmallIntegerField(default=0)
    available_bikes = models.PositiveSmallIntegerField(default=0)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Method returning a simple description of the object"""

        return self.name
