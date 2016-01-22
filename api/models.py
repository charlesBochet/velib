# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Station(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    banking = models.BooleanField()
    bonus = models.BooleanField()
    status = models.CharField(max_length=6)
    contract_name = models.CharField(max_length=15)
    bike_stands = models.PositiveSmallIntegerField(default=0)
    available_bike_stands = models.PositiveSmallIntegerField(default=0)
    available_bikes = models.PositiveSmallIntegerField(default=0)
    optimal_criterion = models.FloatField()
    last_update = models.DateTimeField()
    modified_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        """Method returning a simple description of the object"""

        return self.name
