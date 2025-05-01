from rest_framework import serializers

from airport.serializers import RouteShortSerializer
from cargo.models import CargoFlight, CargoAirplane, Cargo


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            "id",
            "description",
            "weight",
            "volume"
        )


class CargoListSerializer(serializers.ModelSerializer):
    shorted_description = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = (
            "id",
            "shorted_description",
            "weight",
            "volume",
            "is_delivered",
            "condition"
        )

    @staticmethod
    def get_shorted_description(obj):
        return obj.shorted_description


class CargoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            "id",
            "description",
            "weight",
            "volume",
            "is_delivered",
            "condition"
        )


class CargoShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            "id",
            "weight",
            "volume",
        )


class CargoAirplaneShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoAirplane
        fields = (
            "model",
            "registration_number",
        )


class CargoAirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoAirplane
        fields = (
            "id",
            "model",
            "registration_number",
            "country_of_origin",
            "fuel_type",
            "max_cargo_capacity",
            "cargo_hold_volume",
            "max_range_km",
        )


class CargoFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoFlight
        fields = (
            "route",
            "cargo_airplane",
            "departure_time",
            "arrival_time",
        )


class CargoFlightListSerializer(serializers.ModelSerializer):
    route = RouteShortSerializer()
    airplane = CargoAirplaneShortSerializer()

    class Meta:
        model = CargoFlight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )
