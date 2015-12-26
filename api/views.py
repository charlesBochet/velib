# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from api.models import Station
import requests
import csv
import io
from geopy.distance import vincenty


# Create your views here.
def home(request):
    """Home page view"""
    return render(request, 'api/bdd_check.html', locals())


def pulldata(request):
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
            record = Station(number = int(row[0]),
                            name = row[1],
                            address = row[2],
                            lat = float(row[3].split(', ')[0]),
                            lng = float(row[3].split(', ')[1]),
                            banking = bool(row[4]),
                            bonus = bool(row[5]),
                            status = row[6],
                            contract_name = row[7],
                            bike_stands = int(row[8]),
                            available_bike_stands = int(row[9]),
                            available_bikes = int(row[10]),
                            last_update = row[11],
                            modified_date = timezone.now()
                            )
            record.save()
            row_count += 1
    return render(request, 'api/pulldata.html', {'row_count': row_count})


def getstation(request, lat, lng):
    """Returns closest velib station"""
    destination_geopoint = (float(lat), float(lng))
    stations = Station.objects.all()
    min_distance = (999999999, 999999999, 'Unknown')
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
    return HttpResponse(min_distance)