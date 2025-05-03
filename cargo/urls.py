from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cargo.views import (
    CargoViewSet,
    CargoAirplaneViewSet,
    CargoFlightViewSet
)

router = DefaultRouter()

router.register("my-cargos", CargoViewSet)
router.register("cargo-airplanes", CargoAirplaneViewSet)
router.register("cargo-flights", CargoFlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "cargo"
