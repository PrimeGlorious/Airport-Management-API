from rest_framework import serializers

from airport.models import (
    Airport,
    Cargo,
    CargoAirplane,
    Pilot,
    CargoFlight,
    TravelFlight,
    Route,
    TravelAirplane
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


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "source",
            "destination",
            "distance",
        )


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
