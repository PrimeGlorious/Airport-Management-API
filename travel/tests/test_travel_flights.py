from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from airport.models import Airport, Route, Pilot
from travel.models import TravelAirplane, TravelFlight


User = get_user_model()

class TravelFlightAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "pass")
        self.client.force_authenticate(user=self.admin)

        self.source_airport = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.destination_airport = Airport.objects.create(name="JFK", closest_big_city="New York")

        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=4000
        )

        self.pilot = Pilot.objects.create(
            first_name="Jane",
            last_name="Smith",
            badge_number=3002,
            experience=5
        )

        self.airplane = TravelAirplane.objects.create(
            model="A321",
            registration_number="TRV456",
            country_of_origin="USA",
            fuel_type="Jet A",
            max_range_km=8000,
            rows=25,
            seats_in_row=6
        )

    def get_list_url(self):
        return reverse("travel:travelflight-list")

    def get_detail_url(self, pk):
        return reverse("travel:travelflight-detail", kwargs={"pk": pk})

    def test_create_valid_flight(self):
        dep = timezone.now() + timedelta(days=1)
        arr = dep + timedelta(hours=5)
        data = {
            "route": self.route.id,
            "travel_airplane": self.airplane.id,
            "pilots": [self.pilot.id],
            "departure_time": dep.isoformat(),
            "arrival_time": arr.isoformat()
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_overlapping_flight_prevention(self):
        base_time = timezone.now() + timedelta(days=2)
        flight = TravelFlight.objects.create(
            route=self.route,
            travel_airplane=self.airplane,
            departure_time=base_time,
            arrival_time=base_time + timedelta(hours=3)
        )
        flight.pilots.set([self.pilot])
        data = {
            "route": self.route.id,
            "travel_airplane": self.airplane.id,
            "pilots": [self.pilot.id],
            "departure_time": base_time + timedelta(hours=1),
            "arrival_time": base_time + timedelta(hours=4)
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
