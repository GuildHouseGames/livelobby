from django import forms
from events.models import Event, Reservation
from .settings import BOOKING_TIMES_CHOICES, MAX_SIZE_CHOICES, \
    INITIAL_SIZE_CHOICES


class JoinForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('places',)
        labels = {
            'places': 'Group size (Including yourself)',
        }
        widgets = {
            'places': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': "1",
                    'min': "1",
                    'value': "1"}),
        }


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'game',
            'description',
            'date',
            'time',
            'max_size',
            'initial_size',
            'engagement_type',
            'is_booked')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Event Name'}),
            'game': forms.TextInput(
               attrs={'class': 'form-control',
                      'placeholder': 'Game Name'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control',
                       'rows': '5',
                       'placeholder': 'Event Description'}),
            'date': forms.DateInput(attrs={'class':'datepicker'}),
            'time': forms.Select(attrs={'class': 'select'}, choices=BOOKING_TIMES_CHOICES),
            'initial_size': forms.Select(attrs={'class': 'select'}, choices=INITIAL_SIZE_CHOICES),
            'max_size': forms.Select(attrs={'class': 'select'}, choices=MAX_SIZE_CHOICES),
            'engagement_type': forms.Select(attrs={'class': 'select'}, choices=Event.ENGAGEMENT_TYPE),
        }
        help_texts = {
            'is_booked': "I have booked at Guild",
        }
        labels = {
            'name': 'Event Name',
            'game': 'Game Name',
            'initial_size': 'Starting Players',
            'max_size': 'Maximum Players',
            'engagement_type': 'Game Type',
        }
