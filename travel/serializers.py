from rest_framework import serializers

from airport.serializers import RouteShortSerializer
from travel.models import TravelAirplane, TravelFlight


class TravelAirplaneSerializer(serializers.ModelSerializer):
    capacity = serializers.SerializerMethodField()

    class Meta:
        model = TravelAirplane
        fields = (
            "id",
            "model",
            "registration_number",
            "country_of_origin",
            "fuel_type",
            "max_range_km",
            "capacity"
        )

    @staticmethod
    def get_capacity(obj):
        return obj.capacity


class TravelAirplaneCreateSerializer(TravelAirplaneSerializer):
    class Meta(TravelAirplaneSerializer.Meta):
        fields = TravelAirplaneSerializer.Meta.fields + (
            "rows",
            "seats_in_row"
        )


class TravelAirplaneShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAirplane
        fields = (
            "model",
            "registration_number",
        )


class TravelFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelFlight
        fields = (
            "route",
            "travel_airplane",
            "departure_time",
            "arrival_time",
        )


class TravelFlightListSerializer(serializers.ModelSerializer):
    route = RouteShortSerializer()
    airplane = TravelAirplaneShortSerializer()

    class Meta:
        model = TravelFlight
        fields = (
            "route",
            "travel_airplane",
            "departure_time",
            "arrival_time",
        )
