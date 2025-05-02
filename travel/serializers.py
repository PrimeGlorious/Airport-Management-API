from django.db import transaction
from rest_framework import serializers

from airport.serializers import RouteShortSerializer
from travel.models import TravelAirplane, TravelFlight, TravelOrder, TravelTicket


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
    travel_airplane = TravelAirplaneShortSerializer()

    class Meta:
        model = TravelFlight
        fields = (
            "route",
            "travel_airplane",
            "departure_time",
            "arrival_time",
        )


class TravelTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTicket
        fields = (
            "id",
            "row",
            "seat",
            "travel_flight"
        )
        read_only_fields = ("id",)


class TravelTicketListSerializer(serializers.ModelSerializer):
    short_info = serializers.SerializerMethodField()

    class Meta:
        model = TravelTicket
        fields = (
            "short_info",
        )

    @staticmethod
    def get_short_info(obj):
        return str(obj)


class TravelOrderListSerializer(serializers.ModelSerializer):
    travel_tickets = TravelTicketListSerializer(many=True, read_only=True)

    class Meta:
        model = TravelOrder
        fields = (
            "id",
            "travel_tickets",
            "created_at"
        )


class TravelOrderSerializer(serializers.ModelSerializer):
    travel_tickets = TravelTicketSerializer(many=True)

    class Meta:
        model = TravelOrder
        fields = (
            "id",
            "travel_tickets",
            "created_at"
        )

    def create(self, validated_data):
        tickets_data = validated_data.pop("travel_tickets")
        user = self.context["request"].user

        with transaction.atomic():
            order = TravelOrder.objects.create(user=user, **validated_data)

            for ticket_data in tickets_data:
                TravelTicket.objects.create(order=order, **ticket_data)

        return order
