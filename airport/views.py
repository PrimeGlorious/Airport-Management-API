from rest_framework import viewsets

from airport.models import Airport, Cargo, CargoAirplane, Pilot
from airport.serializers import (
    AirportSerializer,
    CargoSerializer,
    CargoListSerializer,
    CargoDetailSerializer,
    CargoAirplaneSerializer,
    CargoAirplaneDetailSerializer, PilotSerializer, CargoAirplaneCreateSerializer, CargoAirplaneUpdateSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CargoAirplaneDetailSerializer
        elif self.action == "create":
            return CargoAirplaneCreateSerializer
        elif self.action == "update":
            return CargoAirplaneUpdateSerializer
        return CargoAirplaneSerializer


class PilotCreateView(viewsets.ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
