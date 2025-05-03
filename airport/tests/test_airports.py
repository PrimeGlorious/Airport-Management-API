from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from airport.models import Airport


User = get_user_model()


class AirportAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.airport = Airport.objects.create(name="Heathrow", closest_big_city="London")

        self.user = User.objects.create_user(username="user", password="testpass")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")

    def test_list_airports_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/airports/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_airports_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/v1/airport/airports/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airport_as_user(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "JFK", "closest_big_city": "New York"}
        response = self.client.post("/api/v1/airport/airports/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airport_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "JFK", "closest_big_city": "New York"}
        response = self.client.post("/api/v1/airport/airports/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_airport_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/v1/airport/airports/{self.airport.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airport_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/v1/airport/airports/{self.airport.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
