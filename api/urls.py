from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^pulldata$', views.pull_data),
    # On laisse de c�t� pour le moment, �a va venir avec l'API REST
    # url(r'^getstation/coordinates/(?P<lat>[+-]?\d?\d\.?\d*)/(?P<lng>[+-]?\d?\d?\d\.?\d*)$',
    #    views.get_station_coordinates),
    # url(r'^get_station/address/(?P<address>.*)$', views.getstation_address)
]
