from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from airport.models import Pilot


User = get_user_model()


class PilotAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.pilot = Pilot.objects.create(
            first_name="John",
            last_name="Doe",
            badge_number=1111,
            experience=5
        )

    def get_list_url(self):
        return reverse("airport:pilot-list")

    def get_detail_url(self, pk):
        return reverse("airport:pilot-detail", kwargs={"pk": pk})

    def test_list_pilots_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pilots_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_pilot_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.get_detail_url(self.pilot.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["badge_number"], 1111)

    def test_create_pilot_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "badge_number": 2222,
            "experience": 10
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_pilot_as_admin_allowed(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "badge_number": 2222,
            "experience": 10
        }
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pilot.objects.count(), 2)

    def test_update_pilot_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "John",
            "last_name": "Updated",
            "badge_number": 1111,
            "experience": 7
        }
        response = self.client.put(self.get_detail_url(self.pilot.pk), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_pilot_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "first_name": "John",
            "last_name": "Updated",
            "badge_number": 1111,
            "experience": 7
        }
        response = self.client.put(self.get_detail_url(self.pilot.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pilot.refresh_from_db()
        self.assertEqual(self.pilot.last_name, "Updated")

    def test_delete_pilot_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.get_detail_url(self.pilot.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_pilot_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.get_detail_url(self.pilot.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pilot.objects.count(), 0)

    def test_filter_pilots_by_first_name(self):
        self.client.force_authenticate(user=self.user)
        url = self.get_list_url() + "?first_name=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["first_name"], "John")

    def test_filter_pilots_by_last_name(self):
        self.client.force_authenticate(user=self.user)
        url = self.get_list_url() + "?last_name=doe"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["last_name"], "Doe")
