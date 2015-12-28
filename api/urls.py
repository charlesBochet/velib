# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'stations', views.StationViewSet)


urlpatterns = [
    url(r'^$', views.home),
    url(r'^', include(router.urls)),
    url(r'^pulldata$', views.pull_data),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    # On laisse de côté pour le moment, ça va venir avec l'API REST
    # url(r'^getstation/coordinates/(?P<lat>[+-]?\d?\d\.?\d*)/(?P<lng>[+-]?\d?\d?\d\.?\d*)$',
    #    views.get_station_coordinates),
    # url(r'^get_station/address/(?P<address>.*)$', views.getstation_address)
]
