# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Station


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = ('number',
                  'name',
                  'address',
                  'lat',
                  'lng',
                  'banking',
                  'bonus',
                  'status',
                  'contract_name',
                  'bike_stands',
                  'available_bike_stands',
                  'available_bikes',
                  'optimal_filling',
                  'last_update',
                  'modified_date')


class RefreshResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    updated_records = serializers.IntegerField()
    issues = serializers.IntegerField()
    datetime = serializers.DateTimeField()


class GeographicPoint(object):  # Object to manipulate inputs for closest station and itenerary.
    def __init__(self, latitude, longitude, address):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address


class GeographicPointSerializer(serializers.Serializer):  # Useless for this version but leaving it here.
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    address = serializers.CharField(max_length=255, default='')

    def create(self, validated_data):
        return GeographicPoint(**validated_data)


class Itenerary(object):
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination


class ItenerarySerializer(serializers.Serializer):
    origin = StationSerializer()
    destination = StationSerializer()


