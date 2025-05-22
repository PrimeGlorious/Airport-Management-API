from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    PilotViewSet,
    RouteViewSet,
)

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("pilots", PilotViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
