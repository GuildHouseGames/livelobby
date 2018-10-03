from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import LiveLobbyUserCreationForm, LiveLobbyUserChangeForm
from .models import LiveLobbyUser


class LiveLobbyUserAdmin(UserAdmin):
    model = LiveLobbyUser
    add_form = LiveLobbyUserCreationForm
    form = LiveLobbyUserChangeForm


admin.site.register(LiveLobbyUser, LiveLobbyUserAdmin)
