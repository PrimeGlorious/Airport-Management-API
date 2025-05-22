from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from cargo.models import (
    Cargo,
    CargoAirplane,
    CargoFlight,
    CargoOrder
)
from cargo.schemas import cargo_airplane_schema
from cargo.serializers import (
    CargoListSerializer,
    CargoSerializer,
    CargoAirplaneSerializer,
    CargoFlightListSerializer,
    CargoFlightSerializer,
    CargoOrderSerializer,
    CargoOrderListSerializer,
    CargoFlightDetailSerializer,
    CargoOrderDetailSerializer
)
from core.custom.mixins import AirPlaneFilteringMixin


class CargoViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Cargo.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CargoListSerializer

        return CargoSerializer


@cargo_airplane_schema
class CargoAirplaneViewSet(AirPlaneFilteringMixin, viewsets.ModelViewSet):
    queryset = CargoAirplane.objects.all()
    serializer_class = CargoAirplaneSerializer


class CargoFlightViewSet(viewsets.ModelViewSet):
    queryset = CargoFlight.objects.all().order_by(
        "-departure_time"
    ).select_related("cargo_airplane", "route")

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
    queryset = CargoOrder.objects.all().order_by(
        "-created_at"
    ).select_related("flight").prefetch_related("cargos")
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer_class(self):
        if self.action == "list":
            return CargoOrderListSerializer
        elif self.action == "retrieve":
            return CargoOrderDetailSerializer
        return CargoOrderSerializer
