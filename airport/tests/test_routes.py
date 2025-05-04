from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from airport.models import Airport, Route


User = get_user_model()


class RouteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        self.airport1 = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.airport2 = Airport.objects.create(name="SFO", closest_big_city="San Francisco")
        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=560)

    def test_list_routes_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/routes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_routes_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/v1/airport/routes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_route_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/v1/airport/routes/{self.route.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["distance"], 560)

    def test_create_route_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 300
        }
        response = self.client.post("/api/v1/airport/routes/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_route_as_admin_success(self):
        self.client.force_authenticate(user=self.admin)

        new_destination = Airport.objects.create(name="ORD", closest_big_city="Chicago")

        data = {
            "source": self.airport1.id,
            "destination": new_destination.id,
            "distance": 300
        }
        response = self.client.post("/api/v1/airport/routes/", data)
        print("STATUS:", response.status_code)
        print("DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_same_source_destination(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "source": self.airport1.id,
            "destination": self.airport1.id,
            "distance": 100
        }
        response = self.client.post("/api/v1/airport/routes/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_route_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 700
        }
        response = self.client.put(f"/api/v1/airport/routes/{self.route.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_route_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 700
        }
        response = self.client.put(f"/api/v1/airport/routes/{self.route.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.route.refresh_from_db()
        self.assertEqual(self.route.distance, 700)

    def test_delete_route_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/v1/airport/routes/{self.route.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_route_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/airport/routes/{self.route.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Route.objects.count(), 0)

    def test_filter_routes_by_source_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/routes/?source=lax")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn("LAX", response.data["results"][0]["source"])

    def test_filter_routes_by_destination_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/routes/?destination=sfo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn("SFO", response.data["results"][0]["destination"])

    def test_filter_routes_by_min_distance(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/routes/?min_distance=500")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertGreaterEqual(response.data["results"][0]["distance"], 500)

    def test_filter_routes_by_max_distance(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/airport/routes/?max_distance=600")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertLessEqual(response.data["results"][0]["distance"], 600)
