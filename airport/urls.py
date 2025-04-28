from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import AirportViewSet


router = DefaultRouter()
router.register("airports", AirportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
