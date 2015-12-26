from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^pulldata$', views.pulldata),
    url(r'^getstation/coordinates/(?P<lat>[+-]?\d?\d\.?\d*)/(?P<lng>[+-]?\d?\d?\d\.?\d*)$', views.getstation_coordinates),
    url(r'^getstation/address/(?P<address>.*)$', views.getstation_address)
]