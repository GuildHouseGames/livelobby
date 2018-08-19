from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from pytz import timezone


class EventType(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name


class Event(models.Model, ):
    name = models.CharField(max_length=75, default='Event')
    time = models.DateTimeField(null=True)
    location = models.CharField(max_length=75, default='Guild')
    description = models.CharField(max_length=300, null=True, blank=True)
    initial_size = models.PositiveSmallIntegerField(default=0)
    max_size = models.PositiveSmallIntegerField(default=4)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True)

    def clean(self):
        TIME_ZONE = getattr(settings, "TIME_ZONE", "UTC")
        now = datetime.now(timezone(TIME_ZONE))

        if self.time and self.time < now:
            raise ValidationError("The event time must be in the future")

        if self.initial_size > self.max_size:
            raise ValidationError("The initial group size cannot be bigger than the max group size")

    def save(self, *args,**kwargs):
        self.clean()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=75)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def clean(self):
        joined_players = Participant.objects.filter(event=self.event)
        if (joined_players.count() + 1) > self.event.max_size - self.event.initial_size:
            raise ValidationError("The event is full")

    def save(self,*args,**kwargs):
        self.clean()
        super(Participant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name