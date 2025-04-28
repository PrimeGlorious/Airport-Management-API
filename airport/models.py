from django.core.validators import MinValueValidator
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    class Meta:
        unique_together = ("name", "closest_big_city")


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
