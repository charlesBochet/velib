# -*- coding: utf-8 -*-
import requests
import csv
import io
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from django.db import connection

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Station
from .serializers import StationSerializer, RefreshResponse, RefreshResponseSerializer, GeographicPoint, Itenerary,\
    ItenerarySerializer, DistanceStation, DistanceStationSerializer


default_walk = 300


class UndefinedPoint(Exception):
    pass


class NonResolvedAddress(Exception):
    pass


def refresh_stations():
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
                                optimal_criterion=(int(row[10])-((int(row[8]))/2))/((int(row[8]))/2),
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
    return refresh_response


def get_closest_station(option, geographicpoint, radius=999999999, number=1):
    """
    Return closest station following parameters.
    """
    if geographicpoint.latitude is None or geographicpoint.longitude is None:
        geolocator = Nominatim()
        location = geolocator.geocode(geographicpoint.address)
        try:
            geographicpoint.latitude = location.latitude
            geographicpoint.longitude = location.longitude
        except AttributeError:
            raise NonResolvedAddress
    else:
        pass
    geographicpoint_coordinates = (geographicpoint.latitude, geographicpoint.longitude)
    stations = Station.objects.all()
    distancestation_list = []  # List containing all stations in the circle with distance to point.
    if option == 'case0':  # Neither pick or drop
        for s in stations:  # Compute all distances destination from destination to stations.
            if s.status == 'OPEN':
                station_coordinates = (s.lat, s.lng)
                distance = vincenty(geographicpoint_coordinates, station_coordinates).m
                if distance <= int(radius):
                    distancestation_list.append(DistanceStation(distance, s))
                else:
                    pass
            else:
                pass
    elif option == 'pick':
        for s in stations:  # Compute all distances destination from destination to stations.
            if s.status == 'OPEN' and s.available_bikes > 0:
                station_coordinates = (s.lat, s.lng)
                distance = vincenty(geographicpoint_coordinates, station_coordinates).m
                if distance <= int(radius):
                    distancestation_list.append(DistanceStation(distance, s))
                else:
                    pass
            else:
                pass
    elif option == 'drop':  # Drop
        for s in stations:  # Compute all distances destination from destination to stations.
            if s.status == 'OPEN' and s.available_bike_stands > 0:
                station_coordinates = (s.lat, s.lng)
                distance = vincenty(geographicpoint_coordinates, station_coordinates).m
                if distance <= int(radius):
                    distancestation_list.append(DistanceStation(distance, s))
                else:
                    pass
            else:
                pass
    distancestation_list.sort(key=lambda DistanceStation: DistanceStation.distance)
    return distancestation_list[:int(number)]


def get_optimal_station(option, geographicpoint, radius=default_walk, number=1):
    """
    Return optimal station following parameters.
    """
    if geographicpoint.latitude is None or geographicpoint.longitude is None:
        geolocator = Nominatim()
        location = geolocator.geocode(geographicpoint.address)
        try:
            geographicpoint.latitude = location.latitude
            geographicpoint.longitude = location.longitude
        except AttributeError:
            raise NonResolvedAddress
    else:
        pass
    geographicpoint_coordinates = (geographicpoint.latitude, geographicpoint.longitude)
    stations = Station.objects.all()
    distancestation_list = []  # List containing all stations in the circle with distance to point.
    if option == 'pick':  # Pick
        for s in stations:  # Compute all distances destination from destination to stations.
            if s.status == 'OPEN' and s.available_bikes > 0:
                station_coordinates = (s.lat, s.lng)
                distance = vincenty(geographicpoint_coordinates, station_coordinates).m
                if distance <= int(radius):
                    distancestation_list.append(DistanceStation(distance, s))
                else:
                    pass
            else:
                pass
        distancestation_list.sort(key=lambda DistanceStation: (-DistanceStation.station.optimal_criterion, DistanceStation.distance))
    elif option == 'drop': # Drop
        for s in stations:  # Compute all distances destination from destination to stations.
            if s.status == 'OPEN' and s.available_bike_stands > 0:
                station_coordinates = (s.lat, s.lng)
                distance = vincenty(geographicpoint_coordinates, station_coordinates).m
                if distance <= int(radius):
                    distancestation_list.append(DistanceStation(distance, s))
                else:
                    pass
            else:
                pass
        distancestation_list.sort(key=lambda DistanceStation: (DistanceStation.station.optimal_criterion, DistanceStation.distance))
    return distancestation_list[:int(number)]


########################################################################################################################
####################################          API    CALLLS         ####################################################
########################################################################################################################


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'stations': reverse('station-list', request=request, format=format)
    })


@api_view(['GET'])
def stations_refresh(request, format=None):
    """
    Refresh velib station database.
    ---
    # Django rest swagger

    response_serializer: RefreshResponseSerializer
    """
    try:
        refresh_response = refresh_stations()
        serializer = RefreshResponseSerializer(refresh_response)
        return Response(serializer.data)
    except:
        return Response({'False'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def stations_log(request, format=None):
    """
    Log station information in secondary log database.

    """
    #try:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO api_stationlog SELECT (SELECT ifnull(max(number),1) FROM api_stationlog)+number,number,status,available_bike_stands,available_bikes,optimal_criterion,modified_date FROM api_station;")
    response = {'True'}
    return Response(response, status=status.HTTP_200_OK)
    #except:
    #    return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed.
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@api_view(['GET'])
def closest_station(request, format=None):
    """
    Returns the n closest stations from a geographic point.
    Stations are searched within a disk defined by the passed geographic point and a radius.\n
    Geographic point is defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default n value is 1.\n
    Default radius value is infinite.
    ---
    # Django rest swagger

    parameters:
        -   name: latitude
            description: latitude
            required: false
            paramType: query
            type: number
        -   name: longitude
            description: longitude
            required: false
            paramType: query
            type: number
        -   name: address
            description: address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: n
            description: number of results returned
            required: false
            paramType: query
            type: integer
        -   name: r
            description: radius of search area
            required: false
            paramType: query
            type: integer

    response_serializer: DistanceStationSerializer
    """
    try:
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        address = request.query_params.get('address', None)
        radius = request.query_params.get('r', 999999999)
        number = request.query_params.get('n', 1)
        if address is None and (latitude is None or longitude is None):
            raise UndefinedPoint
        geographicpoint = GeographicPoint(latitude, longitude, address)
        serializer = DistanceStationSerializer(get_closest_station('case0', geographicpoint, radius, number), many=True)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def closest_station_pick(request, format=None):
    """
    Returns the n closest stations from a geographic point available for pickup.
    Stations are searched within a disk defined by the passed geographic point and a radius.\n
    Geographic point is defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default n value is 1.\n
    Default radius value is infinite.
    ---
    # Django rest swagger

    parameters:
        -   name: latitude
            description: latitude
            required: false
            paramType: query
            type: number
        -   name: longitude
            description: longitude
            required: false
            paramType: query
            type: number
        -   name: address
            description: address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: n
            description: number of results returned
            required: false
            paramType: query
            type: integer
        -   name: r
            description: radius of search ares
            required: false
            paramType: query
            type: integer

    response_serializer: DistanceStationSerializer
    """
    try:
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        address = request.query_params.get('address', None)
        radius = request.query_params.get('r', 999999999)
        number = request.query_params.get('n', 1)
        if address is None and (latitude is None or longitude is None):
            raise UndefinedPoint
        geographicpoint = GeographicPoint(latitude, longitude, address)
        serializer = DistanceStationSerializer(get_closest_station('pick', geographicpoint, radius, number), many=True)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def closest_station_drop(request, format=None):
    """
    Returns the n closest stations from a geographic point available for dropoff.
    Stations are searched within a disk defined by the passed geographic point and a radius.\n
    Geographic point is defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default n value is 1.\n
    Default radius value is infinite.
    ---
    # Django rest swagger

    parameters:
        -   name: latitude
            description: latitude
            required: false
            paramType: query
            type: number
        -   name: longitude
            description: longitude
            required: false
            paramType: query
            type: number
        -   name: address
            description: address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: n
            description: number of results returned
            required: false
            paramType: query
            type: integer
        -   name: r
            description: radius of search area
            required: false
            paramType: query
            type: integer

    response_serializer: DistanceStationSerializer
    """
    try:
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        address = request.query_params.get('address', None)
        radius = request.query_params.get('r', 999999999)
        number = request.query_params.get('n', 1)
        if address is None and (latitude is None or longitude is None):
            raise UndefinedPoint
        geographicpoint = GeographicPoint(latitude, longitude, address)
        serializer = DistanceStationSerializer(get_closest_station('drop', geographicpoint, radius, number), many=True)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def optimal_station_pick(request, format=None):
    """
    Returns the n over optimal stations from a geographic point available for pickup.
    Stations are searched within a disk defined by the passed geographic point and a radius.\n
    Geographic point is defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default n value is 1.\n
    Default radius value is 300m.
    ---
    # Django rest swagger

    parameters:
        -   name: latitude
            description: latitude
            required: false
            paramType: query
            type: number
        -   name: longitude
            description: longitude
            required: false
            paramType: query
            type: number
        -   name: address
            description: address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: n
            description: number of results returned
            required: false
            paramType: query
            type: integer
        -   name: r
            description: radius of search area
            required: false
            paramType: query
            type: integer

    response_serializer: DistanceStationSerializer
    """
    try:
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        address = request.query_params.get('address', None)
        radius = request.query_params.get('r', default_walk)
        number = request.query_params.get('n', 1)
        if address is None and (latitude is None or longitude is None):
            raise UndefinedPoint
        geographicpoint = GeographicPoint(latitude, longitude, address)
        serializer = DistanceStationSerializer(get_optimal_station('pick', geographicpoint, radius, number), many=True)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def optimal_station_drop(request, format=None):
    """
    Returns the n under optimal stations from a geographic point available for dropoff.
    Stations are searched within a disk defined by the passed geographic point and a radius.\n
    Geographic point is defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default n value is 1.\n
    Default radius value is 300m.
    ---
    # Django rest swagger

    parameters:
        -   name: latitude
            description: latitude
            required: false
            paramType: query
            type: number
        -   name: longitude
            description: longitude
            required: false
            paramType: query
            type: number
        -   name: address
            description: address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: n
            description: number of results returned
            required: false
            paramType: query
            type: integer
        -   name: r
            description: radius of search area
            required: false
            paramType: query
            type: integer

    response_serializer: DistanceStationSerializer
    """
    try:
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        address = request.query_params.get('address', None)
        radius = request.query_params.get('r', default_walk)
        number = request.query_params.get('n', 1)
        if address is None and (latitude is None or longitude is None):
            raise UndefinedPoint
        geographicpoint = GeographicPoint(latitude, longitude, address)
        serializer = DistanceStationSerializer(get_optimal_station('drop', geographicpoint, radius, number), many=True)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def closest_itinerary(request, format=None):
    """
    Returns stations 2 stations for itinerary following closest available station logic.
    Geographic points are defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    ---
    # Django rest swagger

    parameters:
        -   name: a-latitude
            description: origin point latitude
            required: false
            paramType: query
            type: number
        -   name: a-longitude
            description: origin point longitude
            required: false
            paramType: query
            type: number
        -   name: a-address
            description: origin point address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: b-latitude
            description: destination point latitude
            required: false
            paramType: query
            type: number
        -   name: b-longitude
            description: destination point longitude
            required: false
            paramType: query
            type: number
        -   name: b-address
            description: destination point address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string

    response_serializer: ItenerarySerializer
    """
    try:
        origin_latitude = request.query_params.get('a-latitude', None)
        origin_longitude = request.query_params.get('b-longitude', None)
        origin_address = request.query_params.get('a-address', None)
        destination_latitude = request.query_params.get('b-latitude', None)
        destination_longitude = request.query_params.get('b-longitude', None)
        destination_address = request.query_params.get('b-address', None)
        if origin_address is None and (origin_latitude is None or origin_longitude is None):
            raise UndefinedPoint
        if destination_address is None and (destination_latitude is None or destination_longitude is None):
            raise UndefinedPoint
        origin_geographicpoint = GeographicPoint(origin_latitude, origin_longitude, origin_address)
        destination_geographicpoint = GeographicPoint(destination_latitude, destination_longitude, destination_address)
        itinerary = Itenerary(get_closest_station('pick', origin_geographicpoint)[0],
                              get_closest_station('drop', destination_geographicpoint)[0])
        serializer = ItenerarySerializer(itinerary)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def optimal_itinerary(request, format=None):
    """
    Returns stations 2 stations for itinerary following under and over optimal station log.
    Geographic points are defined by either address or (latitude,longitude).\n
    If both are passed, only (latitude,longitude) is used.\n
    Default radius value is 300m.
    ---
    # Django rest swagger

    parameters:
        -   name: a-latitude
            description: origin point latitude
            required: false
            paramType: query
            type: number
        -   name: a-longitude
            description: origin point longitude
            required: false
            paramType: query
            type: number
        -   name: a-address
            description: origin point address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: b-latitude
            description: destination point latitude
            required: false
            paramType: query
            type: number
        -   name: b-longitude
            description: destination point longitude
            required: false
            paramType: query
            type: number
        -   name: b-address
            description: destination point address (alphanumeric and whitespace only)
            required: false
            paramType: query
            type: string
        -   name: r
            description: radius of search area
            required: false
            paramType: query
            type: integer

    response_serializer: ItenerarySerializer
    """
    try:
        origin_latitude = request.query_params.get('a-latitude', None)
        origin_longitude = request.query_params.get('b-longitude', None)
        origin_address = request.query_params.get('a-address', None)
        destination_latitude = request.query_params.get('b-latitude', None)
        destination_longitude = request.query_params.get('b-longitude', None)
        destination_address = request.query_params.get('b-address', None)
        radius = request.query_params.get('r', default_walk)
        if origin_address is None and (origin_latitude is None or origin_longitude is None):
            raise UndefinedPoint
        if destination_address is None and (destination_latitude is None or destination_longitude is None):
            raise UndefinedPoint
        origin_geographicpoint = GeographicPoint(origin_latitude, origin_longitude, origin_address)
        destination_geographicpoint = GeographicPoint(destination_latitude, destination_longitude, destination_address)
        itinerary = Itenerary(get_optimal_station('pick', origin_geographicpoint, radius, 1)[0],
                              get_optimal_station('drop', destination_geographicpoint, radius, 1)[0])
        serializer = ItenerarySerializer(itinerary)
        return Response(serializer.data)
    except UndefinedPoint:
        return Response({'Undefined geographical point'}, status=status.HTTP_400_BAD_REQUEST)
    except NonResolvedAddress:
        return Response({'Address not found'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'False'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
