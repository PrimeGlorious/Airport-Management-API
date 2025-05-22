from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
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

    def get_list_url(self):
        return reverse("airport:airport-list")

    def get_detail_url(self, pk):
        return reverse("airport:airport-detail", kwargs={"pk": pk})

    def test_list_airports_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_airports_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_airport_as_user(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "JFK", "closest_big_city": "New York"}
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airport_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "JFK", "closest_big_city": "New York"}
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_airport_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.get_detail_url(self.airport.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airport_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.get_detail_url(self.airport.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_airports_by_name(self):
        self.client.force_authenticate(user=self.user)
        url = self.get_list_url() + "?name=heath"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Heathrow")

    def test_filter_airports_by_city(self):
        self.client.force_authenticate(user=self.user)
        url = self.get_list_url() + "?city=London"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["closest_big_city"], "London")
