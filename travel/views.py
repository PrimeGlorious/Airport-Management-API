from rest_framework import viewsets

from travel.models import TravelFlight, TravelAirplane, TravelOrder
from travel.serializers import (
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneCreateSerializer,
    TravelAirplaneSerializer, TravelOrderSerializer, TravelOrderListSerializer
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


class TravelOrderViewSet(viewsets.ModelViewSet):
    queryset = TravelOrder.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TravelOrderListSerializer
        return TravelOrderSerializer
