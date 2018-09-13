from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from users.forms import LiveLobbyUserCreationForm

class SignUpView(generic.CreateView):
    form_class = LiveLobbyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
