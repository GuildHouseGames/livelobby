from django.contrib import admin
from events.models import Event, Participant, EventType

# Register your models here.
admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Participant)
