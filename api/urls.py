# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^pulldata$', views.pull_data),
    # On laisse de côté pour le moment, ça va venir avec l'API REST
    # url(r'^getstation/coordinates/(?P<lat>[+-]?\d?\d\.?\d*)/(?P<lng>[+-]?\d?\d?\d\.?\d*)$',
    #    views.get_station_coordinates),
    # url(r'^get_station/address/(?P<address>.*)$', views.getstation_address)
]
