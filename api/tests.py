from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from api.models import Station
from api.views import refresh_stations


# Create your tests here.

########################################################################################################################
####################################          Test Unitaire        ####################################################
########################################################################################################################


class StationTest(TestCase):
    """
    Test unitaire du modèle Station
    """
    def test_station(self):
        station_test = Station(number=901,
                        name="00901 - PORT SOLFERINO (STATION MOBILE)",
                        address="QUAI ANATOLE FRANCE - PONT SOLFERINO - 75007 PARIS",
                        lat=48.86138,
                        lng=2.32442,
                        banking=True,
                        bonus=True,
                        status="OPEN",
                        contract_name="Paris",
                        bike_stands=20,
                        available_bike_stands=7,
                        available_bikes=12,
                        optimal_criterion=0.2,
                        last_update="2016-01-24T19:17:50Z",
                        modified_date="2016-01-24T19:26:28.424Z")
        self.assertEqual(str(station_test), "00901 - PORT SOLFERINO (STATION MOBILE)")


########################################################################################################################
####################################      Tests Refresh Database    ####################################################
########################################################################################################################


class RefreshTest(TestCase):
    """
    Test la fonction refresh_stations
    """
    def test_refresh(self):
        refreshed_db = refresh_stations()
        self.assertEqual(refreshed_db.issues, 0)


########################################################################################################################
####################################           Tests Vues           ####################################################
########################################################################################################################


class ViewsTest(TestCase):
    """
    Test les différentes vues
    """
    def setUp(self):
        self.Client = Client()

    def test_vue_docs(self):
        response = self.Client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)


########################################################################################################################
####################################             Tests API          ####################################################
########################################################################################################################


class APITest(APITestCase):
    """
    Test les différentes fonctions de l'API sur deux points fixés
    """
    def setUp(self):
        self.Client = APIClient()
        self.lat_origin = 48.85794
        self.long_origin = 2.34701005
        self.lat_destination = 48.85946238
        self.long_destination = 2.301961227
        refresh_stations()

    def test_api_root(self):
        response = self.Client.get('')
        self.assertEqual(response.status_code, 200)

    def test_refresh(self):
        response = self.Client.get('/api/stations/refresh')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], True)

    def test_closest(self):
        response = self.Client.get('/api/stations/closest', {'latitude': self.lat_origin, 'longitude': self.long_origin})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0], None)

    def test_closest_pick(self):
        response = self.Client.get('/api/stations/closest/pick', {'latitude': self.lat_origin, 'longitude': self.long_origin})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0], None)

    def test_closest_drop(self):
        response = self.Client.get('/api/stations/closest/drop', {'latitude': self.lat_origin, 'longitude': self.long_origin})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0], None)

    def test_optimal_pick(self):
        response = self.Client.get('/api/stations/optimal/pick', {'latitude': self.lat_origin, 'longitude': self.long_origin})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0], None)

    def test_optimal_drop(self):
        response = self.Client.get('/api/stations/optimal/drop', {'latitude': self.lat_origin, 'longitude': self.long_origin})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0], None)

    def test_closest_itinerary(self):
        response = self.Client.get('/api/stations/itinerary/closest', {'a-latitude': self.lat_origin,
                                                                       'a-longitude': self.long_origin,
                                                                       'b-latitude': self.lat_destination,
                                                                       'b-longitude': self.long_destination})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['destination'], None)
        self.assertNotEqual(response.data['origin'], None)

    def test_optimal_itinerary(self):
        response = self.Client.get('/api/stations/itinerary/optimal', {'a-latitude': self.lat_origin,
                                                                       'a-longitude': self.long_origin,
                                                                       'b-latitude': self.lat_destination,
                                                                       'b-longitude': self.long_destination})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['destination'], None)
        self.assertNotEqual(response.data['origin'], None)

