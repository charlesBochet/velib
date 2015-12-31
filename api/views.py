# -*- coding: utf-8 -*-
import requests
import csv
import io
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer, RefreshResponseSerializer, GeographicPoint




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
                             optimal_filling=int(int(row[9])/2),
                             last_update=row[11],
                             modified_date=timezone.now()
                             )
            record.save()
            row_count += 1
    return render(request, 'api/pull_data.html', {'row_count': row_count})


@api_view(['GET'])
def stations_refresh(request, format=None):
    """
    Pulls all velib data from opendata.paris.fr and refresh Velib database.
    """
    class RefreshResponse(object):
        def __init__(self, status, updated_records, issues):
            self.status = status
            self.updated_records = updated_records
            self.issues = issues
            self.datetime = datetime.now()

    try:
        session = requests.Session()
        opendata_url = 'http://opendata.paris.fr/api' \
                        '/records/1.0/download/?dataset=stations-velib-disponibilites-en-temps-reel'
        response = session.get(opendata_url, timeout=10)
        csv_response = io.StringIO(response.text)  # Decode data for csv parser.
        csv_reader = csv.reader(csv_response, delimiter=';')
        refresh_count = 0  # Number of records correctly updated.
        issue_count = 0  # Number of records not updated.
        for row in csv_reader:
            if csv_reader.line_num == 1:
                pass
            else:
                try:
                    record = Station(   number=int(row[0]),
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
                                        optimal_filling=int(int(row[9])/2),
                                        last_update=row[11],
                                        modified_date=timezone.now()
                                    )
                    record.save()
                    refresh_count += 1
                except:
                    issue_count += 1
        if issue_count == 0:
            refresh_response = RefreshResponse(True, refresh_count, 0)
        else:
            refresh_response = RefreshResponse(False, refresh_count, issue_count)
        serializer = RefreshResponseSerializer(refresh_response)
        return Response(serializer.data)
    except:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed.
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer


def get_closest_available_station(geographicpoint):
    """Returns closest opened and non empty velib station from a GeographicPoint object."""
    if geographicpoint.latitude is None or geographicpoint.longitude is None:
        geolocator = Nominatim()
        location = geolocator.geocode(geographicpoint.address)
        geographicpoint.latitude = location.latitude
        geographicpoint.longitude = location.longitude
    else:
        pass
    destination_coordinates = (geographicpoint.latitude, geographicpoint.longitude)
    stations = Station.objects.all()
    min_distance = (999999999, 999999999)  # Initialization : min distance is set to infinite.
    for s in stations:  # Compute all distances destination from destination to stations.
        if s.status == 'OPEN' and s.available_bike_stands > 0:
            station_coordinates = (s.lat, s.lng)
            distance = vincenty(destination_coordinates, station_coordinates).m
            if distance < min_distance[1]:
                min_distance = (s.number, distance)
            else:
                pass
        else:
            pass
    return Station.objects.get(number=min_distance[0])


@api_view(['GET'])
def closest_station(request, latitude=None, longitude=None, address=None):
    geographicpoint = GeographicPoint(latitude, longitude, address)
    serializer = StationSerializer(get_closest_available_station(geographicpoint))
    return Response(serializer.data)
