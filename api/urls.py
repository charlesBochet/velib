# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'stations', views.StationViewSet)


urlpatterns = [
    url(r'^$', views.api_root),

    # Refresh all velib data.
    url(r'^stations/refresh$', views.stations_refresh),

    # Get closest opened stations from a point defined by address or coordinates.
    # Parameter r : defines a circle in which stations closest stations are searched.
    # Parameter n : number of results returned in ranked order (from closest to farthest).
    url(r'^stations/closest/(?P<address>[\s\w]+)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<address>[\s\w]+)/n=(?P<number>n=\d*)/r=(?P<radius>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<address>[\s\w]+)/n=(?P<number>\d*)/?$', views.closest_station_2),


    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/r=(?P<radius>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/?$', views.closest_station_2),
    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/?$', views.closest_station_2),


    # Get closest opened stations from a point defined by coordinates or address for pickup (with available bikes).
    url(r'^stations/closest/pick/(?P<address>[\s\w]+)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<address>[\s\w]+)/n=(?P<number>n=\d*)/r=(?P<radius>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<address>[\s\w]+)/n=(?P<number>\d*)/?$', views.closest_station_pick),


    url(r'^stations/closest/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/?$', views.closest_station_pick),
    url(r'^stations/closest/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/?$', views.closest_station_pick),


    # Get closest opened stations from a point defined by coordinates or address for dropoff (with available stands).
    url(r'^stations/closest/drop/(?P<address>[\s\w]+)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<address>[\s\w]+)/n=(?P<number>n=\d*)/r=(?P<radius>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<address>[\s\w]+)/n=(?P<number>\d*)/?$', views.closest_station_drop),

    url(r'^stations/closest/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/r=(?P<radius>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/?$', views.closest_station_drop),
    url(r'^stations/closest/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/?$', views.closest_station_drop),


    # Get over-optimal opened stations from a point defined by coordinates or address for pickup.
    url(r'^stations/optimal/pick/(?P<address>[\s\w]+)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<address>[\s\w]+)/n=(?P<number>n=\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<address>[\s\w]+)/n=(?P<number>\d*)/?$', views.optimal_station_pick),

    url(r'^stations/optimal/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_pick),
    url(r'^stations/optimal/pick/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/?$', views.optimal_station_pick),


    # Get under-optimal opened stations from a point defined by coordinates or address for drop-off.
    url(r'^stations/optimal/drop/(?P<address>[\s\w]+)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<address>[\s\w]+)/n=(?P<number>n=\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<address>[\s\w]+)/r=(?P<radius>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<address>[\s\w]+)/n=(?P<number>\d*)/?$', views.optimal_station_drop),

    url(r'^stations/optimal/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/n=(?P<number>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/r=(?P<radius>\d*)/?$', views.optimal_station_drop),
    url(r'^stations/optimal/drop/(?P<latitude>[+-]?\d?\d\.?\d*),(?P<longitude>[+-]?\d?\d?\d\.?\d*)/n=(?P<number>\d*)/?$', views.optimal_station_drop),


    # Get optimal station from a point defined by coordinates or address.
#    url(r'^stations/optimal/(?P<latitude>[+-]?\d?\d\.?\d*),'
#        r'(?P<longitude>[+-]?\d?\d?\d\.?\d*)$', views.optimal_station),
#    url(r'^stations/optimal/(?P<address>.*)/$', views.optimal_station),
#
#    # Get itenerary with closest point logic from two points defined by either coordinates or address.
#    # coordinates/coordinates
#    url(r'^stations/itenerary/closest/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
#        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
#        views.closest_itenerary),
#    # address/coordinates
#    url(r'^stations/itenerary/closest/(?P<origin_address>.*)/'
#        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
#        views.closest_itenerary),
#    # coordinates/address
#    url(r'^stations/itenerary/closest/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
#        r'(?P<destination_address>.*)/$', views.closest_itenerary),
#    # address/address
#    url(r'^stations/itenerary/closest/(?P<origin_address>.*)/'
#        r'(?P<destination_address>.*)/$', views.closest_itenerary),
#
#    # Get itenerary with optimal point logic from two points defined by either coordinates or address.
#    # coordinates/coordinates
#    url(r'^stations/itenerary/optimal/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
#        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
#        views.optimal_itenerary),
#    # address/coordinates
#    url(r'^stations/itenerary/optimal/(?P<origin_address>.*)/'
#        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
#        views.optimal_itenerary),
#    # coordinates/address
#    url(r'^stations/itenerary/optimal/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
#        r'(?P<destination_address>.*)/$', views.optimal_itenerary),
#    # address/address
#    url(r'^stations/itenerary/optimal/(?P<origin_address>.*)/'
#        r'(?P<destination_address>.*)/$', views.optimal_itenerary),


    ]

urlpatterns = format_suffix_patterns(urlpatterns)  # enables output format can be specified in url.

urlpatterns += [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

