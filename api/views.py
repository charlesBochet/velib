# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from api.models import Station
import requests
import csv
import io
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from rest_framework import viewsets
from .serializers import StationSerializer


# Create your views here.
def home(request):
    """Home page view"""
    return render(request, 'api/home_api.html', locals())


def pull_data(request):
    """Call to refresh velib data from opendata.paris.fr"""
    session = requests.Session()
    opendata_url = 'http://opendata.paris.fr/api' \
                   '/records/1.0/download/?dataset=stations-velib-disponibilites-en-temps-reel'
    response = session.get(opendata_url, timeout=10)
    csv_response = io.StringIO(response.text)
    csv_reader = csv.reader(csv_response, delimiter=';')
    row_count = 0
    for row in csv_reader:
        if csv_reader.line_num == 1:
            pass
        else:
            record = Station(number=int(row[0]),
                             name=row[1],
                             address=row[2],
                             lat=float(row[3].split(', ')[0]),
                             lng=float(row[3].split(', ')[1]),
                             banking=bool(row[4]),
                             bonus=bool(row[5]),
                             status=row[6],
                             contract_name=row[7],
                             bike_stands=int(row[8]),
                             available_bike_stands=int(row[9]),
                             available_bikes=int(row[10]),
                             last_update=row[11],
                             modified_date=timezone.now()
                             )
            record.save()
            row_count += 1
    return render(request, 'api/pull_data.html', {'row_count': row_count})


def get_station_coordinates(request, lat, lng):
    """Returns closest opened and non empty velib station from coordinates"""
    min_distance = get_closest_station_by_coordinates(lat, lng)
    return HttpResponse(min_distance[2])


def get_station_address(request, address):
    """Returns closest velib station from address"""
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    min_distance = get_closest_station_by_coordinates(location.latitude, location.longitude)
    return HttpResponse(min_distance[2])


def get_closest_station_by_coordinates(lat, lng):
    """Returns closest opened and non empty velib station from coordinates"""
    destination_geopoint = (float(lat), float(lng))
    stations = Station.objects.all()
    min_distance = (999999999, 999999999, 'Unknown')  # Initialization : min distance is set to infinite
    for s in stations:  # Compute all distances destination from destination to stations
        if s.status == 'OPEN' and s.available_bike_stands > 0:
            station_geopoint = (s.lat, s.lng)
            distance = vincenty(destination_geopoint, station_geopoint).m
            if distance < min_distance[1]:
                min_distance = (s.number, distance, s.address)
            else:
                pass
        else:
            pass

    return min_distance


class StationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Station.objects.all()[:20]
    serializer_class = StationSerializer
