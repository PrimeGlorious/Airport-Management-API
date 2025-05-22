from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from airport.models import Airport, Route
from cargo.models import CargoAirplane, Cargo, CargoFlight, CargoOrder


User = get_user_model()

class CargoOrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@test.com", "pass")
        self.client.force_authenticate(user=self.user)

        self.source_airport = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.destination_airport = Airport.objects.create(name="JFK", closest_big_city="New York")

        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=4000
        )

        self.airplane = CargoAirplane.objects.create(
            model="AN-124",
            registration_number="URI82029",
            country_of_origin="Ukraine",
            fuel_type="Jet A",
            max_cargo_capacity=120000,
            cargo_hold_volume=1000,
            max_range_km=5000
        )

        self.flight = CargoFlight.objects.create(
            route=self.route,
            cargo_airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=5)
        )

        self.cargo = Cargo.objects.create(
            user=self.user,
            description="Heavy generator",
            weight=10000,
            volume=200
        )

    def get_list_url(self):
        return reverse("cargo:cargoorder-list")

    def test_create_order_valid(self):
        data = {
            "flight": self.flight.id,
            "cargos": [self.cargo.id]
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_exceed_weight_limit(self):
        self.cargo.weight = 999999
        self.cargo.save()
        data = {
            "flight": self.flight.id,
            "cargos": [self.cargo.id]
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exceed_volume_limit(self):
        self.cargo.volume = 999999
        self.cargo.save()
        data = {
            "flight": self.flight.id,
            "cargos": [self.cargo.id]
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_cargos(self):
        data = {
            "flight": self.flight.id,
            "cargos": []
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_foreign_cargo(self):
        other_user = User.objects.create_user("other", "other@test.com", "pass")
        foreign_cargo = Cargo.objects.create(
            user=other_user,
            description="Foreign cargo",
            weight=100,
            volume=10
        )
        data = {
            "flight": self.flight.id,
            "cargos": [foreign_cargo.id]
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_orders(self):
        other_user = User.objects.create_user("other", "other@test.com", "pass")
        other_cargo = Cargo.objects.create(
            user=other_user,
            description="Other cargo",
            weight=200,
            volume=20
        )
        CargoOrder.objects.create(user=other_user, flight=self.flight)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
