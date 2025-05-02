import re

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

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

    def clean(self):
        super().clean()

        if not re.match(r"^[A-Za-z]{3}\d+$", self.registration_number):
            raise ValidationError("Registration number must start with 3 letters followed by numbers.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model} | {self.registration_number}"


class BaseFlight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        abstract = True
