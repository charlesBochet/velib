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

    #Log Stations
    url(r'^stations/log$', views.stations_log),

    #API Calls
    url(r'^stations/closest/?$', views.closest_station),
    url(r'^stations/closest/pick/?$', views.closest_station),
    url(r'^stations/closest/drop/?$', views.closest_station),
    url(r'^stations/optimal/pick/?$', views.optimal_station_pick),
    url(r'^stations/optimal/drop/?$', views.optimal_station_drop),
    url(r'^stations/itinerary/closest/?$', views.closest_itinerary),
    url(r'^stations/itinerary/optimal/?$', views.optimal_itinerary),




    ]

urlpatterns = format_suffix_patterns(urlpatterns)  # enables output format can be specified in url.

urlpatterns += [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]

