from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from airport.models import Airport, Route
from cargo.models import CargoAirplane, CargoFlight

User = get_user_model()

class CargoFlightAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "pass")
        self.client.force_authenticate(user=self.admin)

        self.source_airport = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.destination_airport = Airport.objects.create(name="JFK", closest_big_city="New York")

        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=4000
        )

        self.airplane = CargoAirplane.objects.create(
            model="Boeing 777F",
            registration_number="ABC123",
            country_of_origin="USA",
            fuel_type="Jet A",
            max_cargo_capacity=100000,
            cargo_hold_volume=850,
            max_range_km=9700
        )

    def test_create_valid_flight(self):
        dep = timezone.now() + timedelta(days=1)
        arr = dep + timedelta(hours=5)
        data = {
            "route": self.route.id,
            "cargo_airplane": self.airplane.id,
            "departure_time": dep.isoformat(),
            "arrival_time": arr.isoformat()
        }
        response = self.client.post("/api/v1/cargo/cargo-flights/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_flight_time(self):
        now = timezone.now()
        data = {
            "route": self.route.id,
            "cargo_airplane": self.airplane.id,
            "departure_time": now.isoformat(),
            "arrival_time": now.isoformat()
        }
        response = self.client.post("/api/v1/cargo/cargo-flights/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overlapping_flights(self):
        base_time = timezone.now() + timedelta(days=1)
        CargoFlight.objects.create(
            route=self.route,
            cargo_airplane=self.airplane,
            departure_time=base_time,
            arrival_time=base_time + timedelta(hours=4)
        )
        data = {
            "route": self.route.id,
            "cargo_airplane": self.airplane.id,
            "departure_time": base_time + timedelta(hours=2),
            "arrival_time": base_time + timedelta(hours=6)
        }
        response = self.client.post("/api/v1/cargo/cargo-flights/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_flights(self):
        dep = timezone.now() + timedelta(days=2)
        arr = dep + timedelta(hours=3)
        CargoFlight.objects.create(
            route=self.route,
            cargo_airplane=self.airplane,
            departure_time=dep,
            arrival_time=arr
        )
        response = self.client.get("/api/v1/cargo/cargo-flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
