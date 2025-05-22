from rest_framework import viewsets

from airport.models import (
    Airport,
    Pilot,
    Route,
)
from airport.schemas import route_schema, pilot_schema, airport_schema
from airport.serializers import (
    AirportSerializer,
    PilotSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)


@airport_schema
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


@pilot_schema
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


@route_schema
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        if self.action in {"list", "retrieve"}:
            queryset = queryset.prefetch_related("source", "destination")

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
