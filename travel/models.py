from django.conf import settings
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from airport.models import Route, Pilot
from core.models import (
    BaseAirplane,
    BaseFlight
)


class TravelAirplane(BaseAirplane):
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class TravelFlight(BaseFlight):
    travel_airplane = models.ForeignKey(
        to=TravelAirplane,
        on_delete=models.CASCADE,
    )
    pilots = models.ManyToManyField(
        to=Pilot,
        related_name="travel_flights",
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="travel_flights",
    )

    def clean(self):
        super().clean()

        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time must be before arrival time.")

        overlapping_flights = TravelFlight.objects.filter(
            travel_airplane=self.travel_airplane
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
        return (f"Flight {self.travel_airplane.model}"
                f" -> {self.departure_time}")


class TravelOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Order #{self.id}"


class TravelTicket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    travel_flight = models.ForeignKey(
        to=TravelFlight,
        related_name="travel_tickets",
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        to=TravelOrder,
        related_name="travel_tickets",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("row", "seat", "travel_flight")

    def clean(self):
        super().clean()

        max_rows = self.travel_flight.travel_airplane.rows
        max_seats = self.travel_flight.travel_airplane.seats_in_row

        if self.row not in range(1, max_rows):
            raise ValidationError(f"Row must be in range 1, {max_rows}")
        if self.seat not in range(1, max_seats):
            raise ValidationError(f"Seat must be in range 1, {max_seats}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Ticket #{self.id} (row: {self.row}, "
                f"seat: {self.seat}) Flight #{self.travel_flight.id}")
