from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    cargos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Cargo.objects.all()
    )

    class Meta:
        model = CargoOrder
        fields = (
            "id",
            "flight",
            "cargos"
        )

    def create(self, validated_data):
        cargos = validated_data.pop("cargos")
        if not cargos:
            raise ValidationError(
                "You must provide at least one cargo."
            )
        user = self.context["request"].user

        order = CargoOrder.objects.create(user=user, **validated_data)
        order.cargos.set(cargos)

        airplane = order.flight.cargo_airplane
        total_weight = sum(cargo.weight for cargo in order.cargos.all())
        total_volume = sum(cargo.volume for cargo in order.cargos.all())

        if total_weight > airplane.max_cargo_capacity:
            raise ValidationError(
                f"Total weight of cargo ({total_weight}) exceeds the aircraft's maximum allowable capacity. ({airplane.max_cargo_capacity})."
            )

        if total_volume > airplane.cargo_hold_volume:
            raise ValidationError(
                f"Total volume of cargo ({total_volume}) exceeds the aircraft's maximum allowable capacity. ({airplane.cargo_hold_volume})."
            )

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


class CargoOrderDetailSerializer(serializers.ModelSerializer):
    flight = CargoFlightDetailSerializer()
    cargos = CargoSerializer(many=True, read_only=True)

    class Meta:
        model = CargoOrder
        fields = (
            "id",
            "created_at",
            "flight",
            "cargos"
        )
