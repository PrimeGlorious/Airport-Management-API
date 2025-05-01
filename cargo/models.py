from django.db import models

from config.base.models import (
    BaseAirplane,
    BaseFlight
)


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

    def __str__(self):
        return f"Flight {self.cargo_airplane.model} -> {self.departure_time}"
