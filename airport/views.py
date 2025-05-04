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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="first_name",
            description="Pilot's first name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="last_name",
            description="Pilot's last name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)
class PilotViewSet(viewsets.ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer

    def get_queryset(self):
        queryset = self.queryset

        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if first_name:
            queryset = queryset.filter(
                first_name__icontains=first_name
            )
        if last_name:
            queryset = queryset.filter(
                last_name__icontains=last_name
            )

        return queryset


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="source",
            description="Source location (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="destination",
            description="Destination location (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="min_distance",
            description="Minimum distance of the route in kilometers",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="max_distance",
            description="Maximum distance of the route in kilometers",
            required=False,
            type=OpenApiTypes.INT,
        ),
    ]
)
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        min_distance = self.request.query_params.get("min_distance")
        max_distance = self.request.query_params.get("max_distance")

        if source:
            queryset = queryset.filter(
                source__name__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                destination__name__icontains=destination
            )
        if min_distance:
            queryset = queryset.filter(
                distance__gte=int(min_distance)
            )
        if max_distance:
            queryset = queryset.filter(
                distance__lte=int(max_distance)
            )

        return queryset



    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer
