from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError

from config.base.models import (
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
