from rest_framework import viewsets

from airport.models import Airport, Cargo
from airport.serializers import AirportSerializer, CargoSerializer, CargoListSerializer, CargoDetailSerializer


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
