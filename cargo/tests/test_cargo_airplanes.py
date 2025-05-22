from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from cargo.models import CargoAirplane


User = get_user_model()

class CargoAirplaneAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "pass")
        self.client.force_authenticate(user=self.admin)

    def get_list_url(self):
        return reverse("cargo:cargoairplane-list")

    def get_detail_url(self, pk):
        return reverse("cargo:cargoairplane-detail", kwargs={"pk": pk})

    def test_create_airplane(self):
        data = {
            "model": "C-130",
            "registration_number": "ABC123",
            "country_of_origin": "USA",
            "fuel_type": "Jet A",
            "max_cargo_capacity": 30000,
            "cargo_hold_volume": 200,
            "max_range_km": 5000
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_capacity(self):
        data = {
            "model": "InvalidPlane",
            "registration_number": "XYZ789",
            "country_of_origin": "Nowhere",
            "fuel_type": "Jet A",
            "max_cargo_capacity": -1,
            "cargo_hold_volume": 100,
            "max_range_km": 1000
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_model(self):
        CargoAirplane.objects.create(
            model="Boeing 747",
            registration_number="BDH747",
            country_of_origin="USA",
            fuel_type="Jet A",
            max_cargo_capacity=50000,
            cargo_hold_volume=300,
            max_range_km=10000
        )
        url = self.get_list_url() + "?model=boeing"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["model"], "Boeing 747")
