from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from travel.models import TravelFlight, TravelAirplane, TravelOrder
from travel.serializers import (
    TravelFlightListSerializer,
    TravelFlightSerializer,
    TravelAirplaneCreateSerializer,
    TravelAirplaneSerializer, TravelOrderSerializer, TravelOrderListSerializer, TravelFlightDetailSerializer
)


class TravelFlightViewSet(viewsets.ModelViewSet):
    queryset = TravelFlight.objects.all().order_by("-departure_time")

    def get_serializer_class(self):
        if self.action == "list":
            return TravelFlightListSerializer
        if self.action == "retrieve":
            return TravelFlightDetailSerializer
        return TravelFlightSerializer


class TravelAirplaneViewSet(viewsets.ModelViewSet):
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
        return TravelOrderSerializer
