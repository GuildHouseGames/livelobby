from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=75, default='Event')
    time = models.DateTimeField(null=True)
    location = models.CharField(max_length=75, default='Guild')
    description = models.CharField(max_length=300, null=True, blank=True)
    max_size = models.PositiveSmallIntegerField(default=4)
    initial_size = models.PositiveSmallIntegerField(default=0)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=75)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name