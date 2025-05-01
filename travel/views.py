from rest_framework import viewsets

from travel.models import TravelFlight, TravelAirplane
from travel.serializers import (
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneCreateSerializer,
    TravelAirplaneSerializer
)


class TravelFlightViewSet(viewsets.ModelViewSet):
    queryset = TravelFlight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TravelFlightListSerializer
        return TravelFlightSerializer


class TravelAirplaneViewSet(viewsets.ModelViewSet):
    queryset = TravelAirplane.objects.all()

    def get_serializer_class(self):
        if self.action in {"create", "update"}:
            return TravelAirplaneCreateSerializer
        return TravelAirplaneSerializer
