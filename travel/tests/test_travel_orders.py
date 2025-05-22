from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from airport.models import Airport, Route, Pilot
from travel.models import TravelAirplane, TravelFlight, TravelOrder, TravelTicket

User = get_user_model()

class TravelOrderAPITestCase(APITestCase):
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

        self.pilot = Pilot.objects.create(
            first_name="Anna",
            last_name="Taylor",
            badge_number=3001,
            experience=7
        )

        self.airplane = TravelAirplane.objects.create(
            model="Airbus A320",
            registration_number="TRV123",
            country_of_origin="USA",
            fuel_type="Jet A",
            max_range_km=6000,
            rows=20,
            seats_in_row=6
        )

        self.flight = TravelFlight.objects.create(
            route=self.route,
            travel_airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=5)
        )
        self.flight.pilots.set([self.pilot])

    def get_list_url(self):
        return reverse("travel:travelorder-list")

    def test_create_valid_order_with_ticket(self):
        data = {
            "travel_tickets": [
                {
                    "row": 5,
                    "seat": 3,
                    "travel_flight": self.flight.id
                }
            ]
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TravelOrder.objects.count(), 1)
        self.assertEqual(TravelTicket.objects.count(), 1)

    def test_create_order_with_invalid_seat(self):
        data = {
            "travel_tickets": [
                {
                    "row": 21,
                    "seat": 1,
                    "travel_flight": self.flight.id
                }
            ]
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_tickets(self):
        data = {
            "travel_tickets": []
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_duplicate_seat(self):
        TravelTicket.objects.create(
            row=10,
            seat=4,
            travel_flight=self.flight,
            order=TravelOrder.objects.create(user=self.user)
        )
        data = {
            "travel_tickets": [
                {
                    "row": 10,
                    "seat": 4,
                    "travel_flight": self.flight.id
                }
            ]
        }
        response = self.client.post(self.get_list_url(), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_orders(self):
        other_user = User.objects.create_user("other", "other@test.com", "pass")
        other_order = TravelOrder.objects.create(user=other_user)
        TravelTicket.objects.create(
            row=3,
            seat=2,
            travel_flight=self.flight,
            order=other_order
        )
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
