from abc import abstractclassmethod

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} | {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_to")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} -> {self.destination.name}"


class Pilot(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    badge_number = models.PositiveIntegerField(unique=True)
    experience = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Cargo(models.Model):
    class ConditionChoices(models.TextChoices):
        GOOD = "good", "Good"
        DAMAGED = "damaged", "Damaged"

    description = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    is_delivered = models.BooleanField(default=False)
    condition = models.CharField(
        max_length=7,
        choices=ConditionChoices,
        default=ConditionChoices.GOOD,
    )

    def __str__(self):
        return (f"Weight {self.weight} Volume {self.volume} "
                f"| is delivered = {self.is_delivered}")

    @property
    def shorted_description(self):
        return self.description[:40]


class BaseAirplane(models.Model):
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    country_of_origin = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    max_range_km = models.PositiveIntegerField(
        validators=[
            MinValueValidator(50)
        ]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.model} | {self.registration_number}"


class CargoAirplane(BaseAirplane):
    max_cargo_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    cargo_hold_volume = models.DecimalField(max_digits=6, decimal_places=2)
    cargos = models.ManyToManyField(
        Cargo,
        related_name="cargo_airplanes",
        blank=True,
    )


class TravelAirplane(BaseAirplane):
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class BaseFlight(models.Model):
    route = models.OneToOneField(
        Route,
        on_delete=models.CASCADE,
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        abstract = True


class CargoFlight(BaseFlight):
    cargo_airplane = models.ForeignKey(
        to=CargoAirplane,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Flight {self.cargo_airplane.model} -> {self.departure_time}"


class TravelFlight(BaseFlight):
    travel_airplane = models.ForeignKey(
        to=TravelAirplane,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Flight {self.travel_airplane.model} -> {self.departure_time}"
