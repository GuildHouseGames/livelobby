from django import forms
from events.models import Participant


class JoinForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name','event')
        widgets = {
            'name': forms.TextInput(
                attrs={ 'class':'form-control',
                        'placeholder':'Player name'}),
            'event': forms.HiddenInput()
        }