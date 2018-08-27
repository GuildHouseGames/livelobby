from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from pytz import timezone
import sys
from datetime import date

class EventType(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=75, default='Event')
    date = models.DateField(db_index=True, null=True)
    time = models.TimeField(db_index=True, null=True)
    location = models.CharField(max_length=75, default='Guild')
    description = models.CharField(max_length=300, null=True, blank=True)
    initial_size = models.PositiveSmallIntegerField(default=0)
    max_size = models.PositiveSmallIntegerField(default=4)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True)

    def clean(self):
        # size validation
        if self.initial_size > self.max_size:
            raise ValidationError("The initial group size cannot be bigger than the max group size")
        if not self.max_size > self.initial_size:
            raise ValidationError("The max group size must be larger than the initial group size")

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
                raise ValidationError("For a booking today, the time must be in the future")

    def save(self, *args,**kwargs):
        self.clean()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=75)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    hosted_event = models.OneToOneField(Event, related_name="+", on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        joined_players = Participant.objects.filter(event=self.event)
        # Compare the players who have joined this event (excluding the host)
        # combined with those who were already in the event, with the max size
        if (joined_players.count()-1 + self.event.initial_size >= self.event.max_size):
            raise ValidationError("Unfortunately the event is full")

    def save(self,*args,**kwargs):
        self.clean()
        super(Participant, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
