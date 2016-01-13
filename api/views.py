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
from rest_framework.reverse import reverse

from .models import Station
from .serializers import StationSerializer, RefreshResponseSerializer, GeographicPoint, Itenerary, ItenerarySerializer




# Create your views here.
def home(request):
    """Home page view"""
    return render(request, 'api/home_api.html', locals())


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'stations': reverse('station-list', request=request, format=format)
    })


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
    min_station = (999999999, 999999999)  # Initialization : min distance is set to infinite.
    for s in stations:  # Compute all distances destination from destination to stations.
        if s.status == 'OPEN' and s.available_bike_stands > 0:
            station_coordinates = (s.lat, s.lng)
            distance = vincenty(destination_coordinates, station_coordinates).m
            if distance < min_station[1]:
                min_station = (s.number, distance)
            else:
                pass
        else:
            pass
    return Station.objects.get(number=min_station[0])

def get_optimal_nearby_station(geographicpoint, radius=200):
    """Returns the optimal velib station inside a specified radius (200 m by default )from a GeographicPoint object."""
    if geographicpoint.latitude is None or geographicpoint.longitude is None:
        geolocator = Nominatim()
        location = geolocator.geocode(geographicpoint.address)
        geographicpoint.latitude = location.latitude
        geographicpoint.longitude = location.longitude
    else:
        pass
    destination_coordinates = (geographicpoint.latitude, geographicpoint.longitude)
    stations = Station.objects.all()
    nearby_stations = [] # Initialization of the array containing the velib stations inside the radius
    for s in stations:  # Compute all distances destination from destination to stations.
        if s.status == 'OPEN' and s.available_bike_stands > 0:
            station_coordinates = (s.lat, s.lng)
            distance = vincenty(destination_coordinates, station_coordinates).m
            if distance < radius:
                nearby_stations.append((s.number, distance, s.bike_stands, s.available_bike_stands, 1 - s.available_bike_stands/s.bike_stands))
            else:
                pass
        else:
            pass
    sorted_nearby_stations = sorted(nearby_stations, key= lambda station: station[4])
    opt_station = sorted_nearby_stations[0] #The optimal station by default is the least occupied
    for s in sorted_nearby_stations: #If there are more than one least occupied stations, the optimal one is the closest one)
        if s[1] < opt_station[1] and s[4] == opt_station[4]:
            opt_station = s
        else:
            pass
    return Station.objects.get(number=opt_station[0])

@api_view(['GET'])
def closest_station(request, latitude=None, longitude=None, address=None):
    geographicpoint = GeographicPoint(latitude, longitude, address)
    serializer = StationSerializer(get_closest_available_station(geographicpoint))
    return Response(serializer.data)


@api_view(['GET'])
def optimal_station(request, latitude=None, longitude=None, address=None):
    geographicpoint = GeographicPoint(latitude, longitude, address)
    serializer = StationSerializer(get_optimal_nearby_station(geographicpoint))
    return Response(serializer.data)


@api_view(['GET'])
def closest_itenerary(request, origin_latitude=None, origin_longitude=None, origin_address=None,
                destination_latitude=None, destination_longitude=None, destination_address=None):
    origin_geographicpoint = GeographicPoint(origin_latitude, origin_longitude, origin_address)
    destination_geographicpoint = GeographicPoint(destination_latitude, destination_longitude, destination_address)
    itenerary = Itenerary(get_closest_available_station(origin_geographicpoint),
                          get_closest_available_station(destination_geographicpoint))
    serializer = ItenerarySerializer(itenerary)
    return Response(serializer.data)


@api_view(['GET'])
def optimal_itenerary(request, origin_latitude=None, origin_longitude=None, origin_address=None,
                destination_latitude=None, destination_longitude=None, destination_address=None):
    origin_geographicpoint = GeographicPoint(origin_latitude, origin_longitude, origin_address)
    destination_geographicpoint = GeographicPoint(destination_latitude, destination_longitude, destination_address)
    distance = vincenty((origin_latitude, origin_longitude, origin_address), (destination_latitude, destination_longitude, destination_address)).m
    itenerary = Itenerary(get_closest_available_station(origin_geographicpoint),
                          get_optimal_nearby_station(destination_geographicpoint, distance/10))
    serializer = ItenerarySerializer(itenerary)
    return Response(serializer.data)

