from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from users.models import LiveLobbyUser
from django.shortcuts import redirect
from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login to 
    perform some actions right after successful login
    '''
    def pre_social_login(self, request, sociallogin):
        pass

# @receiver(pre_social_login)
# def link_to_local_user(sender, request, sociallogin, **kwargs):
#     email_address = sociallogin.account.extra_data['email']
#     users = LiveLobbyUser.objects.filter(email=email_address)
#     if users:
#         # users[0].profile_picture = sociallogin.account.extra_data
#         perform_login(request, users[0], email_verification='None')
#         raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))

# @receiver(pre_social_login)
# def update_profile_picture(sender, request, sociallogin, **kwargs):
#     sender.profile_picture = sociallogin.account.extra_data['profile']