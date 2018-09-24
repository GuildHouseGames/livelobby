from datetime import datetime, timedelta
from time import time
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from events.forms import JoinForm
from events.models import Event, Participant
from pytz import timezone
from faker import Faker

class ParticipantTest(TestCase):

    def setUp(self):
        self.time = datetime.now() + timedelta(1)
        self.fake = Faker()

    def test_participants_can_join_open_events(self):
        max_size = 5
        # Participants can join whenever theres a spot free no matter what the initial size is
        for initial_size in range(max_size):
            event = Event.objects.create(initial_size=initial_size, max_size=max_size,time=self.time.time(), date=self.time.date())
            available_spots = max_size - initial_size
            for _ in range(available_spots):
                Participant.objects.create(event=event)
            self.assertEqual(available_spots, Participant.objects.filter(event=event).count())
            event.delete()

    def test_participants_cannot_join_full_events(self):
        with self.assertRaises(ValidationError) as e:
            event = Event.objects.create(initial_size=1,max_size=1, time=self.time.time(), date=self.time.date())
            Participant.objects.create(event=event)
            Participant.objects.create(event=event)
        self.assertEqual(e.exception.message, "Unfortunately the event is full")

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
            Event.objects.create(time=datetime.now().time(), date=datetime.now().date() - timedelta(1))
        self.assertEqual(e.exception.message, "The date must be in the future")

    def test_future_event_date(self):
        event = Event.objects.create(time=datetime.now().time(), date=datetime.now().date() + timedelta(1))
        # The event was successfully created
        self.assertTrue(isinstance(event, Event))

    def test_initial_size_larger_than_max(self):
        time = datetime.now() + timedelta(1)
        with self.assertRaises(ValidationError) as e:
            initial_size = 2
            max_size = 1
            Event.objects.create(max_size=max_size, initial_size=initial_size, date=time.date(), time=time.time())
        self.assertEqual(e.exception.message, "The initial group size cannot be bigger than the max group size")

    def test_valid_initial_and_max_size(self):
        size = 1
        time = datetime.now() + timedelta(1)
        a = Event.objects.create(initial_size=size, max_size=size,  date=time.date(), time=time.time())
        b = Event.objects.create(initial_size=size, max_size=size+1, date=time.date(), time=time.time())
        # The events were successfully created
        self.assertTrue(isinstance(a, Event))
        self.assertTrue(isinstance(b, Event))

    def test_to_str(self):
        name = self.fake.name()
        time = datetime.now() + timedelta(1)
        event = Event.objects.create(name=name, date=time.date(), time=time.time())
        self.assertEqual(name,str(event))

class JoinFormTest(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.time = datetime.now() + timedelta(1)

    def test_blank_name(self):
        event = Event.objects.create(time=self.time.time(), date=self.time.date())
        data = {'event': event.pk}
        form = JoinForm(data=data)
        self.assertFalse(form.is_valid())

    def test_open_event(self):
        event = Event.objects.create(time=self.time.time(), date=self.time.date())
        data = {'name': self.fake.name(), 'event': event.pk}
        form = JoinForm(data=data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_full_event(self):
        event = Event.objects.create(initial_size=1, max_size=1, time=self.time.time(), date=self.time.date())
        data = {'name': self.fake.name(), 'event': event.pk}
        form = JoinForm(data=data)
        self.assertFalse(form.is_valid())