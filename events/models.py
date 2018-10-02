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

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=75, default='Event')
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

    is_cancelled = models.BooleanField(default=False)

    def clean(self):
        # size validation
        if self.initial_size > self.max_size:
            raise ValidationError(
                "The initial group size cannot be bigger"
                " than the max group size")
        if not self.max_size >= self.initial_size:
            raise ValidationError(
                "The max group size must be larger than"
                " the initial group size")

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

    def save(self, *args, **kwargs):
        self.clean()
        super(Event, self).save(*args, **kwargs)
        # Create the event with an initial reservation for the host
        if self.initial_size > 0:
            Reservation.objects.create(
                user=self.host, event=self, places=self.initial_size)

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
        if (self.event.reserved_places() + self.places > self.event.max_size):
            raise ValidationError(
                "The specified number of places exceeds the "
                "number of places available")
        if Reservation.objects.filter(event=self.event, user=self.user):
            raise ValidationError("This event has already been joined")
        if self.event.is_cancelled:
            raise ValidationError("This event has been cancelled.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Reservation, self).save(*args, **kwargs)
