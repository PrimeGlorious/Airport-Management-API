from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from config.custom.mixins import AirPlaneFilteringMixin
from travel.models import TravelFlight, TravelAirplane, TravelOrder
from travel.serializers import (
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneCreateSerializer,
    TravelAirplaneSerializer, TravelOrderSerializer, TravelOrderListSerializer, TravelFlightDetailSerializer,
    TravelOrderCreateSerializer
)


class TravelFlightViewSet(viewsets.ModelViewSet):
    queryset = TravelFlight.objects.all().order_by("-departure_time")

    def get_serializer_class(self):
        if self.action == "list":
            return TravelFlightListSerializer
        if self.action == "retrieve":
            return TravelFlightDetailSerializer
        return TravelFlightSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="min_range",
            description="Minimum range (km) the airplane can fly",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="max_range",
            description="Maximum range (km) the airplane can fly",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="model",
            description="Model name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="country",
            description="Country of origin (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)
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
    queryset = TravelOrder.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TravelOrderListSerializer
        elif self.action == "create":
            return TravelOrderCreateSerializer
        return TravelOrderSerializer
