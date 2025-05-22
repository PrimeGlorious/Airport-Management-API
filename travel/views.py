from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.custom.mixins import AirPlaneFilteringMixin
from travel.models import TravelFlight, TravelAirplane, TravelOrder
from travel.schemas import travel_airplane_schema
from travel.serializers import (
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneCreateSerializer,
    TravelAirplaneSerializer, TravelOrderSerializer, TravelOrderListSerializer, TravelFlightDetailSerializer,
    TravelOrderCreateSerializer
)


class TravelFlightViewSet(viewsets.ModelViewSet):
    queryset = TravelFlight.objects.all().order_by(
        "-departure_time"
    ).select_related(
        "travel_airplane", "route"
    ).prefetch_related(
        "pilots"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return TravelFlightListSerializer
        if self.action == "retrieve":
            return TravelFlightDetailSerializer
        return TravelFlightSerializer


@travel_airplane_schema
class TravelAirplaneViewSet(AirPlaneFilteringMixin, viewsets.ModelViewSet):
    queryset = TravelAirplane.objects.all()

    def get_serializer_class(self):
        if self.action in {"create", "update"}:
            return TravelAirplaneCreateSerializer
        return TravelAirplaneSerializer


class TravelOrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TravelOrder.objects.all().order_by(
        "-created_at"
    ).prefetch_related("travel_tickets")
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TravelOrderListSerializer
        elif self.action == "create":
            return TravelOrderCreateSerializer
        return TravelOrderSerializer
