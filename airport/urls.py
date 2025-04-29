from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import AirportViewSet, CargoViewSet, CargoAirplaneViewSet, PilotCreateView

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("cargos", CargoViewSet)
router.register("cargo_airplanes", CargoAirplaneViewSet)
router.register("pilots", PilotCreateView)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
