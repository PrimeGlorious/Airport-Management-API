from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from airport.models import Route
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
        return f"Weight {self.weight} Volume {self.volume}"

    @property
    def shorted_description(self):
        if len(self.description) > 40:
            return self.description[:40] + "..."
        return self.description


class CargoAirplane(BaseAirplane):
    max_cargo_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    cargo_hold_volume = models.DecimalField(max_digits=6, decimal_places=2)
    cargos = models.ManyToManyField(
        Cargo,
        related_name="cargo_airplanes",
        blank=True,
    )


class CargoFlight(BaseFlight):
    cargo_airplane = models.ForeignKey(
        to=CargoAirplane,
        on_delete=models.CASCADE,
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="cargo_flights",
    )

    def __str__(self):
        return f"Flight {self.cargo_airplane.model} -> {self.departure_time}"
