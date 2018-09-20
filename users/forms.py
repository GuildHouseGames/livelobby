from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LiveLobbyUser

class LiveLobbyUserCreationForm(UserCreationForm):

    display_name = forms.CharField(max_length=30, help_text='Your name as shown to other users')

    class Meta(UserCreationForm.Meta):
        model = LiveLobbyUser
        fields = ('username', 'email', 'display_name')

class LiveLobbyUserChangeForm(UserChangeForm):

    class Meta:
        model = LiveLobbyUser
        fields = UserChangeForm.Meta.fields