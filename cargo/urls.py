from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cargo.views import (
    CargoViewSet,
    CargoAirplaneViewSet,
    CargoFlightViewSet, CargoOrderViewSet
)

router = DefaultRouter()

router.register("my-cargos", CargoViewSet)
router.register("cargo-airplanes", CargoAirplaneViewSet)
router.register("cargo-flights", CargoFlightViewSet)
router.register("my-orders", CargoOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "cargo"
