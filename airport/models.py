from django.core.validators import MinValueValidator
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    class Meta:
        unique_together = ("name", "closest_big_city")


class Pilot(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    badge_number = models.PositiveIntegerField(unique=True)
    experience = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ]
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


class CargoAirplane(models.Model):
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    country_of_origin = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20)
    max_cargo_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    cargo_hold_volume = models.DecimalField(max_digits=6, decimal_places=2)
    max_range_km = models.PositiveIntegerField(
        validators=[
            MinValueValidator(50)
        ]
    )
    cargos = models.ManyToManyField(
        Cargo,
        related_name="cargo_airplanes",
        blank=True,
    )
    pilots = models.ManyToManyField(
        to=Pilot,
        related_name="cargo_airplanes",
        blank=True,
    )
    is_active = models.BooleanField(default=False)
