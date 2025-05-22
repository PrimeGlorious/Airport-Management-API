from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from travel.models import TravelAirplane


User = get_user_model()

class TravelAirplaneAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "pass")
        self.client.force_authenticate(user=self.admin)

    def get_list_url(self):
        return reverse("travel:travelairplane-list")

    def test_create_valid_airplane(self):
        data = {
            "model": "A350",
            "registration_number": "TRV001",
            "country_of_origin": "USA",
            "fuel_type": "Jet A",
            "max_range_km": 15000,
            "rows": 30,
            "seats_in_row": 6
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_registration_number(self):
        data = {
            "model": "A320",
            "registration_number": "123ABC",
            "country_of_origin": "USA",
            "fuel_type": "Jet A",
            "max_range_km": 10000,
            "rows": 25,
            "seats_in_row": 6
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_model(self):
        TravelAirplane.objects.create(
            model="Boeing 787",
            registration_number="TRV777",
            country_of_origin="USA",
            fuel_type="Jet A",
            max_range_km=14000,
            rows=40,
            seats_in_row=8
        )
        url = self.get_list_url() + "?model=boeing"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
