from rest_framework import serializers

from airport.models import Airport, Cargo, CargoAirplane, Pilot, Flight, Route


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


class CargoAirplaneShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoAirplane
        fields = (
            "model",
            "registration_number",
        )


class CargoAirplaneSerializer(serializers.ModelSerializer):
    cargos_count = serializers.SerializerMethodField()

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
            "cargos_count",
        )

    def get_cargos_count(self, obj):
        return obj.cargos.count()


class CargoAirplaneCreateSerializer(serializers.ModelSerializer):
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


class CargoAirplaneUpdateSerializer(CargoAirplaneCreateSerializer):
    class Meta(CargoAirplaneCreateSerializer.Meta):
        fields = CargoAirplaneCreateSerializer.Meta.fields + (
            "cargos",
        )


class CargoAirplaneDetailSerializer(CargoAirplaneCreateSerializer):
    cargos = CargoShortSerializer(many=True, read_only=True)

    class Meta(CargoAirplaneCreateSerializer.Meta):
        fields = CargoAirplaneCreateSerializer.Meta.fields + ("cargos",)


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


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(serializers.ModelSerializer):
    route = RouteShortSerializer()
    airplane = CargoAirplaneShortSerializer()

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )
