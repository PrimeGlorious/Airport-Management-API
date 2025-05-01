from django.core.validators import MinValueValidator
from django.db import models

from airport.models import Route


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


class BaseFlight(models.Model):
    route = models.OneToOneField(
        Route,
        on_delete=models.CASCADE,
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        abstract = True
