from rest_framework import serializers

from airport.serializers import RouteShortSerializer, RouteSerializer
from cargo.models import CargoFlight, CargoAirplane, Cargo, CargoOrder


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
    cargo_airplane = CargoAirplaneShortSerializer()

    class Meta:
        model = CargoFlight
        fields = (
            "id",
            "route",
            "cargo_airplane",
            "departure_time",
            "arrival_time",
        )


class CargoFlightDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    cargo_airplane = CargoAirplaneSerializer()

    class Meta:
        model = CargoFlight
        fields = (
            "id",
            "route",
            "cargo_airplane",
            "departure_time",
            "arrival_time",
        )


class CargoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoOrder
        fields = (
            "id",
            "flight",
            "cargos"
        )

    def create(self, validated_data):
        user = self.context["request"].user
        order = CargoOrder.objects.create(user=user, **validated_data)
        return order


class CargoOrderListSerializer(serializers.ModelSerializer):
    flight = CargoFlightListSerializer()
    cargos_count = serializers.SerializerMethodField()

    class Meta:
        model = CargoOrder
        fields = (
            "id",
            "created_at",
            "flight",
            "cargos_count"
        )

    @staticmethod
    def get_cargos_count(obj):
        return obj.cargos.count()
