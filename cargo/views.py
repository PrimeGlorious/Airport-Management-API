from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from cargo.models import (
    Cargo,
    CargoAirplane,
    CargoFlight,
    CargoOrder
)
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


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CargoListSerializer

        return CargoSerializer


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
class CargoAirplaneViewSet(viewsets.ModelViewSet):
    queryset = CargoAirplane.objects.all()
    serializer_class = CargoAirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset

        min_range = self.request.query_params.get("min_range")
        max_range = self.request.query_params.get("max_range")
        model = self.request.query_params.get("model")
        country = self.request.query_params.get("country")

        if min_range:
            queryset = queryset.filter(
                max_range_km__gte=int(min_range),
            )
        if max_range:
            queryset = queryset.filter(
                max_range_km__lte=int(max_range),
            )
        if model:
            queryset = queryset.filter(
                model__icontains=model,
            )
        if country:
            queryset = queryset.filter(
                country_of_origin__icontains=country,
            )

        return queryset



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
