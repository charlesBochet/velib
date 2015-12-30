# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Station


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('number', 'name', 'address', 'lat', 'lng', 'banking', 'bonus', 'status',
                  'contract_name', 'bike_stands', 'available_bike_stands', 'available_bikes',
                  'last_update', 'modified_date')

class RefreshResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    updated_records = serializers.IntegerField()
    issues = serializers.IntegerField()
    datetime = serializers.DateTimeField()