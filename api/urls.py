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
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # Refresh all velib data.
    url(r'^stations/refresh$', views.stations_refresh),

    # Get closest station from a point defined by coordinates or address.
    url(r'^stations/closest/(?P<latitude>[+-]?\d?\d\.?\d*),'
        r'(?P<longitude>[+-]?\d?\d?\d\.?\d*)$', views.closest_station),
    url(r'^stations/closest/(?P<address>.*)$', views.closest_station),

    # Get optimal station from a point defined by coordinates or address.
    url(r'^stations/optimal/(?P<latitude>[+-]?\d?\d\.?\d*),'
        r'(?P<longitude>[+-]?\d?\d?\d\.?\d*)$', views.optimal_station),
    url(r'^stations/optimal/(?P<address>.*)$', views.optimal_station),

    # Get itenerary with closest point logic from two points defined by either coordinates or address.
    # coordinates/coordinates
    url(r'^stations/itenerary/closest/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
        views.closest_itenerary),
    # address/coordinates
    url(r'^stations/itenerary/closest/(?P<origin_address>.*)/'
        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
        views.closest_itenerary),
    # coordinates/address
    url(r'^stations/itenerary/closest/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
        r'(?P<destination_address>.*)$', views.closest_itenerary),
    # address/address
    url(r'^stations/itenerary/closest/(?P<origin_address>.*)/'
        r'(?P<destination_address>.*)$', views.closest_itenerary),

    # Get itenerary with optimal point logic from two points defined by either coordinates or address.
    # coordinates/coordinates
    url(r'^stations/itenerary/optimal/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
        views.optimal_itenerary),
    # address/coordinates
    url(r'^stations/itenerary/optimal/(?P<origin_address>.*)/'
        r'(?P<destination_latitude>[+-]?\d?\d\.?\d*),(?P<destination_longitude>[+-]?\d?\d?\d\.?\d*)$',
        views.optimal_itenerary),
    # coordinates/address
    url(r'^stations/itenerary/optimal/(?P<origin_latitude>[+-]?\d?\d\.?\d*),(?P<origin_longitude>[+-]?\d?\d?\d\.?\d*)/'
        r'(?P<destination_address>.*)$', views.optimal_itenerary),
    # address/address
    url(r'^stations/itenerary/optimal/(?P<origin_address>.*)/'
        r'(?P<destination_address>.*)$', views.optimal_itenerary),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)  # enables output format can be specified in url.

urlpatterns += [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
