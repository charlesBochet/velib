from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from api.models import Station
from api.views import refresh_stations
from rest_framework.test import APIRequestFactory

# Create your tests here.

########################################################################################################################
####################################          Base    Tests         ####################################################
########################################################################################################################


class RefreshTest(TestCase):
    """
    Test la fonction refresh_stations
    """
    def test_refresh(self):
        refreshed_db = refresh_stations()
        self.assertEqual(refreshed_db.issues, 0)


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
####################################           Tests vues           ####################################################
########################################################################################################################


class ViewsTest(APITestCase):
    def setUp(self):
        self.Client = APIClient()

    def Test_vue(self):
        response = self.Client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)


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