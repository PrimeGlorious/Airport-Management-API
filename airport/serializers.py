from rest_framework import serializers

from airport.models import (
    Airport,
    Pilot,
    Route,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
        )


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = (
            "id",
            "first_name",
            "last_name",
            "badge_number",
            "experience"
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)


class RouteShortSerializer(serializers.ModelSerializer):
    travel = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            "travel",
            "distance",
        )

    @staticmethod
    def get_travel(obj):
        return str(obj)
