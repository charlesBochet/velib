from django.db import models


class Article(models.Model):
    number = models.PositiveIntegerField()
    contract_name = models.CharField(max_length=15)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()
    banking = models.BooleanField()
    bonus = models.BooleanField()
    status = models.CharField(max_length=6)
    bike_stands = models.PositiveSmallIntegerField()
    available_bike_stands = models.PositiveSmallIntegerField
    available_bikes = models.PositiveSmallIntegerField
    last_update = models.DateTimeField

    def __str__(self):
        """Method returning a simple description of the object"""

        return self.titre
