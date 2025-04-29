from rest_framework import serializers

from airport.models import Airport, Cargo, CargoAirplane, Pilot


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


class CargoAirplaneSerializer(serializers.ModelSerializer):
    cargos_count = serializers.SerializerMethodField()
    pilots_count = serializers.SerializerMethodField()

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
            "pilots_count",
            "is_active",
        )

    def get_cargos_count(self, obj):
        return obj.cargos.count()

    def get_pilots_count(self, obj):
        return obj.pilots.count()


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
            "pilots",
            "is_active",
        )


class CargoAirplaneDetailSerializer(CargoAirplaneCreateSerializer):
    cargos = CargoShortSerializer(many=True, read_only=True)
    pilots = PilotSerializer(many=True, read_only=True)

    class Meta(CargoAirplaneCreateSerializer.Meta):
        fields = CargoAirplaneCreateSerializer.Meta.fields + ("cargos", "pilots", "is_active",)
