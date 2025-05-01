from rest_framework import viewsets

from cargo.models import Cargo, CargoAirplane, CargoFlight
from cargo.serializers import CargoListSerializer, CargoDetailSerializer, CargoSerializer, CargoAirplaneSerializer, \
    CargoFlightListSerializer, CargoFlightSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CargoListSerializer
        elif self.action == "retrieve":
            return CargoDetailSerializer

        return CargoSerializer


class CargoAirplaneViewSet(viewsets.ModelViewSet):
    queryset = CargoAirplane.objects.all()
    serializer_class = CargoAirplaneSerializer


class CargoFlightViewSet(viewsets.ModelViewSet):
    queryset = CargoFlight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CargoFlightListSerializer
        return CargoFlightSerializer
