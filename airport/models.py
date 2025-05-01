from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} | {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_from")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="route_to")
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ("source", "destination")

    def clean(self):
        super().clean()

        if self.source == self.destination:
            raise ValidationError("Source and destination must be different")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
