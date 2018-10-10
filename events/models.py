from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime
from django.db.models import Sum
from pytz import timezone
from datetime import date


class Event(models.Model):
    TYPE_CHOICES = (
        ("GAME", "Game"),
    )

    ENGAGEMENT_TYPE = (
        ("COMPETITIVE", "Competitive"),
        ("CASUAL", "Casual"),
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=75, default='Event')
    game = models.CharField(max_length=75, default='Monopoly')
    date = models.DateField(db_index=True, null=True)
    time = models.TimeField(db_index=True, null=True)
    location = models.CharField(max_length=75, default='Guild')
    description = models.CharField(max_length=300, null=True, blank=True)
    initial_size = models.PositiveSmallIntegerField(default=1)
    max_size = models.PositiveSmallIntegerField(default=1)

    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="GAME"
    )

    engagement_type = models.CharField(
        max_length=25,
        choices=ENGAGEMENT_TYPE,
        default="CASUAL"
    )

    is_cancelled = models.BooleanField(default=False)

    is_booked = models.BooleanField(default=False)

    def clean(self):
        # size validation
        if self.initial_size > self.max_size:
            raise ValidationError(
                "The starting players size cannot be larger"
                " than the maximum players size")
        if not self.max_size >= self.initial_size:
            raise ValidationError(
                "The maximum players size must be larger than"
                " the starting players size")

        # date and time validation
        TIME_ZONE = getattr(settings, "TIME_ZONE", "UTC")
        now = datetime.now(timezone(TIME_ZONE))
        if not self.time:
            raise ValidationError("The time must be entered")
        if not self.date:
            raise ValidationError("The date must be entered")
        if (self.date < date.today()):
            raise ValidationError("The date must be in the future")
        if (self.date == date.today()):
            if (self.time < now.time()):
                raise ValidationError(
                    "For a booking today, the time must be in the future")

        # If we are updating the event, we cannot modify the initial/max size
        # if that modification would fill the event based on already made
        # reservations.
        reservation = Reservation.objects.filter(event=self, user=self.host).first()
        if reservation:
            if (self.reserved_places() - reservation.places + self.initial_size > self.max_size):
                if (self.initial_size <= reservation.places):
                    raise ValidationError("Cannot reduce the size of the event as reservations have already filled the event.")
                else:
                    raise ValidationError("Cannot increase the number of starting players as reservations have already filled the event.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Event, self).save(*args, **kwargs)
        # Create the event with an initial reservation for the host
        if self.initial_size > 0:
            reservation = Reservation.objects.filter(user=self.host, event=self).first()
            # If this event already has a reservation just update it, if not create one
            if not reservation:
                Reservation.objects.create(
                    user=self.host, event=self, places=self.initial_size)
            else:
                reservation.places=self.initial_size
                reservation.save()

    def player_list(self):
        players = Reservation.objects.filter(event=self)
        return players

    def reserved_places(self):
        reservations = Reservation.objects.filter(event=self)
        return reservations.aggregate(
            Sum('places'))["places__sum"] if reservations else 0

    def is_joined(self, user):
        reservations = Reservation.objects.filter(event=self, user=user)
        return reservations is not None and reservations.count() > 0

    def __str__(self):
        return self.name


class Reservation(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    places = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def clean(self):
        if self.event.is_cancelled:
            raise ValidationError("This event has been cancelled.")
        if Reservation.objects.filter(event=self.event, user=self.user):
            if not self.event.host == self.user:
                raise ValidationError("This event has already been joined")

        # Validation for join only
        if not self.event.host == self.user:
            if (self.event.reserved_places() + self.places > self.event.max_size):
                raise ValidationError(
                    "The specified number of places exceeds the "
                    "number of places available")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Reservation, self).save(*args, **kwargs)
