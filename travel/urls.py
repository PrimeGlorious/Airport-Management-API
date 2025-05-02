from django.urls import path, include
from rest_framework import routers

from travel.views import (
    TravelAirplaneViewSet,
    TravelFlightViewSet,
    TravelOrderViewSet
)

router = routers.DefaultRouter()
router.register("travel-airplanes", TravelAirplaneViewSet)
router.register("travel-flights", TravelFlightViewSet)
router.register("my-orders", TravelOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "travel"
