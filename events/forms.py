from django import forms
from events.models import Participant, Event
from .settings import BOOKING_TOMORROW, BOOKING_TIMES_CHOICES,\
    MAX_SIZE_CHOICES, INITIAL_SIZE_CHOICES


class JoinForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'event')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Player name'}),
            'event': forms.HiddenInput()
        }


class CreateEventForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=BOOKING_TIMES_CHOICES, initial='',
        widget=forms.Select(attrs={'class': 'form-control'}), required=True,
        help_text="The time this event will take place"
    )

    date = forms.DateField(
        initial=BOOKING_TOMORROW,
        widget=forms.SelectDateWidget(
                attrs={'class': 'form-control snps-inline-select'}),
        help_text="The date your event will take place"
    )

    max_size = forms.ChoiceField(
        choices=MAX_SIZE_CHOICES,
        help_text="The maximum number of players for this event",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    initial_size = forms.ChoiceField(
        choices=INITIAL_SIZE_CHOICES,
        help_text="The initial number of players for this event"
        "(Including the host, must be below the maximum number of players)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    host = forms.CharField(
        label='Host Name', max_length=75,
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    ' placeholder': 'Host name...'}
                )
        )

    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'time',
                  'max_size', 'initial_size', 'type')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Event name...'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'rows': '5',
                       'placeholder': 'Event description...'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'name': "To help other players find the event they're looking for",
            'description': "Additional information to describe your event"
            "(how long it might take, where you are in the room etc...)",
            'type': 'The type of event (i.e Game)',
            'host': 'The name of the host for this event'
        }
