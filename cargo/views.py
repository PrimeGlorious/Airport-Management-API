from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from cargo.models import Cargo, CargoAirplane, CargoFlight, CargoOrder
from cargo.serializers import CargoListSerializer, CargoSerializer, CargoAirplaneSerializer, \
    CargoFlightListSerializer, CargoFlightSerializer, CargoOrderSerializer, CargoOrderListSerializer, \
    CargoFlightDetailSerializer, CargoOrderDetailSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CargoListSerializer

        return CargoSerializer


class CargoAirplaneViewSet(viewsets.ModelViewSet):
    queryset = CargoAirplane.objects.all()
    serializer_class = CargoAirplaneSerializer


class CargoFlightViewSet(viewsets.ModelViewSet):
    queryset = CargoFlight.objects.all().order_by("-departure_time")

    def get_serializer_class(self):
        if self.action == "list":
            return CargoFlightListSerializer
        elif self.action == "retrieve":
            return CargoFlightDetailSerializer
        return CargoFlightSerializer


class CargoOrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = CargoOrder.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CargoOrderListSerializer
        elif self.action == "retrieve":
            return CargoOrderDetailSerializer
        return CargoOrderSerializer
