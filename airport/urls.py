from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    CargoViewSet,
    CargoAirplaneViewSet,
    PilotViewSet,
    CargoFlightViewSet,
    TravelFlightViewSet,
    RouteViewSet,
    TravelAirplaneViewSet
)

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("cargos", CargoViewSet)
router.register("cargo-airplanes", CargoAirplaneViewSet)
router.register("travel-airplanes", TravelAirplaneViewSet)
router.register("pilots", PilotViewSet)
router.register("cargo-flights", CargoFlightViewSet)
router.register("travel-flights", TravelFlightViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
