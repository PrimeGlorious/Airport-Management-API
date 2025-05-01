from rest_framework import viewsets

from airport.models import (
    Airport,
    Cargo,
    CargoAirplane,
    Pilot,
    CargoFlight,
    TravelFlight,
    Route, TravelAirplane)
from airport.serializers import (
    AirportSerializer,
    CargoSerializer,
    CargoListSerializer,
    CargoDetailSerializer,
    CargoAirplaneSerializer,
    PilotSerializer,
    CargoFlightSerializer,
    CargoFlightListSerializer,
    RouteSerializer,
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneSerializer,
    TravelAirplaneCreateSerializer, RouteListSerializer, RouteDetailSerializer
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
    serializer_class = CargoAirplaneSerializer


class TravelAirplaneViewSet(viewsets.ModelViewSet):
    queryset = TravelAirplane.objects.all()

    def get_serializer_class(self):
        if self.action in {"create", "update"}:
            return TravelAirplaneCreateSerializer
        return TravelAirplaneSerializer


class PilotViewSet(viewsets.ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class CargoFlightViewSet(viewsets.ModelViewSet):
    queryset = CargoFlight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CargoFlightListSerializer
        return CargoFlightSerializer


class TravelFlightViewSet(viewsets.ModelViewSet):
    queryset = TravelFlight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TravelFlightListSerializer
        return TravelFlightSerializer
