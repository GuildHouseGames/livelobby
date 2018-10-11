from django import forms
from events.models import Event, Reservation
from .settings import BOOKING_TIMES_CHOICES, MAX_SIZE_CHOICES, \
    INITIAL_SIZE_CHOICES, MAX_SIZE_CHOICES_EDIT, INITIAL_SIZE_CHOICES_EDIT


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
            'initial_size',
            'max_size',
            'engagement_type',
            'is_booked')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'game': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'rows': '5'}),
            'date': forms.DateInput(
                attrs={
                    'class': 'datepicker'}),
            'time': forms.Select(
                attrs={
                    'class': 'select'},
                choices=BOOKING_TIMES_CHOICES),
            'initial_size': forms.Select(
                attrs={
                    'class': 'select'},
                choices=INITIAL_SIZE_CHOICES),
            'max_size': forms.Select(
                attrs={
                    'class': 'select'},
                choices=MAX_SIZE_CHOICES),
            'engagement_type': forms.Select(
                attrs={
                    'class': 'select'},
                choices=Event.ENGAGEMENT_TYPE),
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

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['name'] = ''
        initial['game'] = ''
        initial['date'] = ''
        kwargs['initial'] = initial
        super(CreateEventForm, self).__init__(*args, **kwargs)


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'game',
            'description',
            'date',
            'time',
            'initial_size',
            'max_size',
            'engagement_type',
            'is_booked')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'game': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'rows': '5'}),
            'date': forms.DateInput(
                attrs={
                    'class': 'datepicker'}),
            'time': forms.Select(
                attrs={
                    'class': 'select'},
                choices=BOOKING_TIMES_CHOICES),
            'initial_size': forms.Select(
                attrs={
                    'class': 'select'},
                choices=INITIAL_SIZE_CHOICES_EDIT),
            'max_size': forms.Select(
                attrs={
                    'class': 'select'},
                choices=MAX_SIZE_CHOICES_EDIT),
            'engagement_type': forms.Select(
                attrs={
                    'class': 'select'},
                choices=Event.ENGAGEMENT_TYPE),
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
