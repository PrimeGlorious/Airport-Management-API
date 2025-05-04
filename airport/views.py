from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from airport.models import (
    Airport,
    Pilot,
    Route,
)
from airport.serializers import (
    AirportSerializer,
    PilotSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="name",
            description="Partial name of the airport (case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="city",
            description="Partial name of the closest big city (case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        city = self.request.query_params.get("city")

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )
        if city:
            queryset = queryset.filter(
                closest_big_city__icontains=city
            )

        return queryset


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
