from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from events.models import Event, Participant
from pytz import timezone
from faker import Faker

class ParticipantTest(TestCase):

    def setUp(self):
        self.fake = Faker()

    def test_participants_can_join_open_events(self):
        max_size = 5
        # Participants can join whenever theres a spot free no matter what the initial size is
        for initial_size in range(max_size):
            event = Event.objects.create(initial_size=initial_size, max_size=max_size)
            available_spots = max_size - initial_size
            for _ in range(available_spots):
                Participant.objects.create(event=event)
            self.assertEqual(available_spots, Participant.objects.filter(event=event).count())
            event.delete()

    def test_participants_cannot_join_full_events(self):
        with self.assertRaises(ValidationError) as e:
            event = Event.objects.create(max_size=1)
            Participant.objects.create(event=event)
            Participant.objects.create(event=event)
        self.assertEqual(e.exception.message, "The event is full")

    def test_to_str(self):
        name = self.fake.name()
        participant = Participant(name=name)
        self.assertEqual(name, str(participant))

class EventTest(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.tz = timezone(getattr(settings, "TIME_ZONE", "UTC"))

    def test_past_event_date(self):
        with self.assertRaises(ValidationError) as e:
            Event.objects.create(time=(datetime.now(self.tz) + timedelta(-1)))
        self.assertEqual(e.exception.message, "The event time must be in the future")

    def test_future_event_date(self):
        time = datetime.now(self.tz) + timedelta(1)
        event = Event.objects.create(time=time)
        # The event was successfully created
        self.assertTrue(isinstance(event, Event))

    def test_initial_size_larger_than_max(self):
        with self.assertRaises(ValidationError) as e:
            initial_size = 2
            max_size = 1
            Event.objects.create(max_size=max_size, initial_size=initial_size)
        self.assertEqual(e.exception.message, "The initial group size cannot be bigger than the max group size")

    def test_valid_initial_and_max_size(self):
        size = 1
        a = Event.objects.create(initial_size=size, max_size=size)
        b = Event.objects.create(initial_size=size, max_size=size+1)
        # The events were successfully created
        self.assertTrue(isinstance(a, Event))
        self.assertTrue(isinstance(b, Event))

    def test_to_str(self):
        name = self.fake.name()
        event = Event.objects.create(name=name)
        self.assertEqual(name,str(event))

class EventType:

    def setUp(self):
        self.fake = Faker()

    def test_to_str(self):
        name = self.fake.name()
        event_type = EventType.objects.create(name=name)
        self.assertEqual(name,str(event_type))
