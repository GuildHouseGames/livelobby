
from django.urls import reverse_lazy
from django.views import generic

from users.forms import LiveLobbyUserCreationForm

from allauth.socialaccount.forms import SignupForm


class SignUpView(generic.CreateView):
    form_class = LiveLobbyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class MyCustomSocialSignupForm(SignupForm):

    def save(self):

        # Ensure you call the parent classes save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save()

        # Add your own processing here.

        # You must return the original result.
        return user
