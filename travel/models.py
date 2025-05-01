from django.db import models

from config.base.models import BaseAirplane, BaseFlight


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
        return f"Flight {self.travel_airplane.model} -> {self.departure_time}"
