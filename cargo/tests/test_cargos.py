from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from cargo.models import Cargo

User = get_user_model()

class CargoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.force_authenticate(user=self.user)

    def get_list_url(self):
        return reverse("cargo:cargo-list")

    def get_detail_url(self, pk):
        return reverse("cargo:cargo-detail", kwargs={"pk": pk})

    def test_create_valid_cargo(self):
        data = {"description": "Box", "weight": 10.5, "volume": 1.2}
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_weight(self):
        data = {"description": "Too heavy", "weight": 10000, "volume": 1}
        response = self.client.post(self.get_list_url(), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_cargos(self):
        other = User.objects.create_user(username="other", password="pass")
        Cargo.objects.create(description="Other", weight=1, volume=1, user=other)
        Cargo.objects.create(description="Mine", weight=2, volume=2, user=self.user)
        response = self.client.get(self.get_list_url())
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["shorted_description"], "Mine")
