from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from airport.models import Route, Pilot
from config.base.models import (
    BaseAirplane,
    BaseFlight
)


class Cargo(models.Model):
    description = models.CharField(max_length=100)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(500)
        ],
    )
    volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
    )

    def __str__(self):
        return (f"{self.shorted_description} || "
                f"Weight {self.weight} Volume {self.volume}")

    @property
    def shorted_description(self):
        if len(self.description) > 40:
            return self.description[:40] + "..."
        return self.description


class CargoAirplane(BaseAirplane):
    max_cargo_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    cargo_hold_volume = models.DecimalField(max_digits=6, decimal_places=2)


class CargoFlight(BaseFlight):
    cargo_airplane = models.ForeignKey(
        to=CargoAirplane,
        on_delete=models.CASCADE,
    )
    pilots = models.ManyToManyField(
        to=Pilot,
        related_name="cargo_flights",
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="cargo_flights",
    )

    def clean(self):
        super().clean()

        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time must be before arrival time.")

        overlapping_flights = CargoFlight.objects.filter(
            cargo_airplane=self.cargo_airplane
        ).exclude(pk=self.pk).filter(
            Q(departure_time__lt=self.arrival_time) &
            Q(arrival_time__gt=self.departure_time)
        )

        if overlapping_flights.exists():
            raise ValidationError("This airplane already has a flight in this time range.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flight {self.cargo_airplane.model} -> {self.departure_time}"


class CargoOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cargo_orders",
    )
    flight = models.ForeignKey(
        to=CargoFlight,
        on_delete=models.CASCADE,
        related_name="cargo_orders",
    )
    cargos = models.ManyToManyField(
        to=Cargo,
        related_name="cargo_orders",
    )
